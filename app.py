"""
Social Media Analysis App - Twitter/X Integration
Multi-agent bias detection with X.com (Twitter) scraping via Twscrape
"""

import streamlit as st
import asyncio
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime
from orchestrator import SocialMediaOrchestrator
from data_structures import Comment
from twscrape import API, gather

# Configure page
st.set_page_config(
    page_title="🎯 Social Media Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Twitter/X configuration
TWITTER_BASE_URL = "https://x.com/"
TWEET_URL_PATTERN = r"https?://(?:twitter\.com|x\.com)/\w+/status/(\d+)"
USER_URL_PATTERN = r"https?://(?:twitter\.com|x\.com)/(\w+)(?:/.*)?$"

def extract_tweet_id(url):
    """Extract tweet ID from Twitter/X URL"""
    match = re.search(TWEET_URL_PATTERN, url)
    return match.group(1) if match else None

def extract_username(url):
    """Extract username from Twitter/X URL"""
    match = re.search(USER_URL_PATTERN, url)
    return match.group(1) if match else None

def check_api_key():
    """Check if API key is configured"""
    return "gemini_api_key" in st.session_state and st.session_state.gemini_api_key

def scrape_user_tweets(username, tweet_count):
    """Wrapper to run async user tweet scraping"""
    asyncio.run(_scrape_user_tweets(username, tweet_count))

def scrape_post_replies(tweet_id, reply_count):
    """Wrapper to run async post reply scraping"""
    asyncio.run(_scrape_post_replies(tweet_id, reply_count))

async def _scrape_user_tweets(username, tweet_count):
    """Scrape tweets from a specific user"""
    try:
        with st.spinner(f"Scraping {tweet_count} tweets from @{username}..."):
            api = API()
            
            # Get user info first
            user = await api.user_by_login(username)
            if not user:
                st.error(f"User @{username} not found or account is private")
                return
            
            st.info(f"Found user: @{user.username} ({user.displayname}) - {user.followersCount} followers")
            
            # Scrape user tweets
            tweets = await gather(api.user_tweets(user.id, limit=tweet_count))
            
            if not tweets:
                st.warning(f"No tweets found for @{username}")
                return
            
            # Convert tweets to Comment objects
            comments = []
            for i, tweet in enumerate(tweets):
                comment = Comment(
                    id=f"tweet_{tweet.id}",
                    text=tweet.rawContent,
                    author_id=str(tweet.user.id),
                    author_username=tweet.user.username,
                    author_bio=tweet.user.description or "",
                    timestamp=tweet.date,
                    metrics={
                        "likes": tweet.likeCount,
                        "retweets": tweet.retweetCount,
                        "replies": tweet.replyCount,
                        "views": tweet.viewCount or 0
                    },
                    author_followers=tweet.user.followersCount,
                    author_verified=tweet.user.verified
                )
                comments.append(comment)
            
            st.success(f"✅ Scraped {len(comments)} tweets from @{username}")
            
            # Show preview
            with st.expander("📄 Scraped Tweets Preview", expanded=False):
                for i, comment in enumerate(comments[:5], 1):
                    st.write(f"**{i}.** {comment.text[:200]}{'...' if len(comment.text) > 200 else ''}")
                    st.write(f"   💖 {comment.metrics['likes']} | 🔄 {comment.metrics['retweets']} | 💬 {comment.metrics['replies']}")
                    st.write("---")
            
            # Run analysis
            await run_analysis_on_comments(comments, f"user_@{username}")
            
    except Exception as e:
        st.error(f"Failed to scrape tweets from @{username}: {str(e)}")
        st.exception(e)

async def _scrape_post_replies(tweet_id, reply_count):
    """Scrape replies from a specific tweet"""
    try:
        with st.spinner(f"Scraping {reply_count} replies from tweet {tweet_id}..."):
            api = API()
            
            # Get original tweet info
            original_tweet = await api.tweet_details(int(tweet_id))
            if not original_tweet:
                st.error(f"Tweet {tweet_id} not found or is not accessible")
                return
            
            st.info(f"Original tweet by @{original_tweet.user.username}: {original_tweet.rawContent[:100]}...")
            
            # Scrape replies
            replies = await gather(api.tweet_replies(int(tweet_id), limit=reply_count))
            
            if not replies:
                st.warning(f"No replies found for tweet {tweet_id}")
                return
            
            # Convert replies to Comment objects
            comments = []
            for i, reply in enumerate(replies):
                comment = Comment(
                    id=f"reply_{reply.id}",
                    text=reply.rawContent,
                    author_id=str(reply.user.id),
                    author_username=reply.user.username,
                    author_bio=reply.user.description or "",
                    timestamp=reply.date,
                    metrics={
                        "likes": reply.likeCount,
                        "retweets": reply.retweetCount,
                        "replies": reply.replyCount,
                        "views": reply.viewCount or 0
                    },
                    author_followers=reply.user.followersCount,
                    author_verified=reply.user.verified
                )
                comments.append(comment)
            
            st.success(f"✅ Scraped {len(comments)} replies from tweet {tweet_id}")
            
            # Show preview
            with st.expander("📄 Scraped Replies Preview", expanded=False):
                for i, comment in enumerate(comments[:5], 1):
                    st.write(f"**{i}.** @{comment.author_username}: {comment.text[:200]}{'...' if len(comment.text) > 200 else ''}")
                    st.write(f"   💖 {comment.metrics['likes']} | 🔄 {comment.metrics['retweets']} | 💬 {comment.metrics['replies']}")
                    st.write("---")
            
            # Run analysis
            await run_analysis_on_comments(comments, f"tweet_{tweet_id}")
            
    except Exception as e:
        st.error(f"Failed to scrape replies from tweet {tweet_id}: {str(e)}")
        st.exception(e)

async def run_analysis_on_comments(comments, source_id):
    """Run the multi-agent analysis on scraped comments"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Initializing orchestrator...")
        orchestrator = SocialMediaOrchestrator(st.session_state.gemini_api_key)
        progress_bar.progress(0.2)
        
        status_text.text("Running multi-agent analysis...")
        post_id = f"twitter_analysis_{source_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = await orchestrator.analyze_post_comments(post_id, comments)
        progress_bar.progress(1.0)
        
        status_text.text("Analysis complete!")
        
        # Save results
        with open("analysis_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        st.success(f"✅ Analysis complete! Processed {len(comments)} comments.")
        st.balloons()
        
        # Show quick results
        with st.expander("📊 Quick Results Preview", expanded=True):
            show_quick_results(results)
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.exception(e)

# Configure page
st.set_page_config(
    page_title="🎯 Social Media Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Twitter/X configuration
TWITTER_BASE_URL = "https://x.com/"
TWEET_URL_PATTERN = r"https?://(?:twitter\.com|x\.com)/\w+/status/(\d+)"
USER_URL_PATTERN = r"https?://(?:twitter\.com|x\.com)/(\w+)(?:/.*)?$"

def extract_tweet_id(url):
    """Extract tweet ID from Twitter/X URL"""
    match = re.search(TWEET_URL_PATTERN, url)
    return match.group(1) if match else None

def extract_username(url):
    """Extract username from Twitter/X URL"""
    match = re.search(USER_URL_PATTERN, url)
    return match.group(1) if match else None

def check_api_key():
    """Check if API key is configured"""
    return "gemini_api_key" in st.session_state and st.session_state.gemini_api_key

def show_quick_results(results):
    """Show condensed results preview"""
    summary = results.get("summary", {})
    risk_assessment = results.get("risk_assessment", {})
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Comments", summary.get("total_comments", 0))
    with col2:
        risk = risk_assessment.get("overall_risk", "unknown")
        risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        st.metric("Risk Level", f"{risk_colors.get(risk, '⚪')} {risk.upper()}")
    with col3:
        st.metric("Flagged", risk_assessment.get("flagged_comments", 0))
    with col4:
        avg_toxicity = summary.get("average_toxicity", 0)
        st.metric("Avg Toxicity", f"{avg_toxicity:.2f}")

def main():
    """Main application"""
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    
    # API Key management
    if not check_api_key():
        with st.sidebar.expander("⚙️ API Configuration", expanded=True):
            api_key = st.text_input("Gemini API Key", type="password", key="api_input")
            if st.button("Save API Key"):
                if api_key:
                    st.session_state.gemini_api_key = api_key
                    st.success("API key saved!")
                    st.rerun()
                else:
                    st.error("Please enter a valid API key")
        st.error("⚠️ Please configure your Gemini API key to continue.")
        return
    
    # Page selection
    page = st.sidebar.selectbox(
        "Choose Page",
        ["📝 Input & Analysis", "📊 Dashboard", "📚 Documentation"],
        key="page_selector"
    )
    
    # Clear data option
    if st.sidebar.button("🗑️ Clear All Results"):
        if os.path.exists("analysis_results.json"):
            os.remove("analysis_results.json")
        st.success("Results cleared!")
        st.rerun()
    
    # Route to appropriate page
    if page == "📝 Input & Analysis":
        show_input_page()
    elif page == "📊 Dashboard":
        show_dashboard_page()
    else:
        show_documentation_page()

def show_input_page():
    """Input and analysis interface"""
    st.title("📝 X.com (Twitter) Analysis")
    st.markdown("Scrape and analyze X.com (Twitter) content for bias, sentiment, and authenticity")
    
    # Input method selection
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 Analyze User Profile", use_container_width=True, type="primary"):
            st.session_state.input_method = "user"
    
    with col2:
        if st.button("📝 Analyze Single Post", use_container_width=True):
            st.session_state.input_method = "post"
    
    st.markdown("---")
    
    # Show selected input method
    if "input_method" not in st.session_state:
        st.session_state.input_method = "user"
    
    if st.session_state.input_method == "user":
        show_user_input()
    elif st.session_state.input_method == "post":
        show_post_input()

def show_user_input():
    """Twitter user profile analysis interface"""
    st.subheader("👤 Twitter User Analysis")
    st.markdown("Analyze recent tweets from a specific Twitter/X user")
    
    # User URL input
    user_url = st.text_input(
        "Twitter/X User URL or Username:",
        placeholder="https://x.com/username or just 'username'",
        help="Enter the full Twitter/X profile URL or just the username"
    )
    
    # Number of tweets to analyze
    tweet_count = st.slider("Number of recent tweets to analyze:", 1, 50, 20)
    
    if st.button("🔍 Scrape & Analyze User Tweets", type="primary", disabled=not user_url.strip()):
        username = extract_username(user_url) if user_url.startswith('http') else user_url.strip().lstrip('@')
        if username:
            scrape_user_tweets(username, tweet_count)
        else:
            st.error("Invalid Twitter/X URL or username format")

def show_post_input():
    """Twitter post analysis interface"""
    st.subheader("� Twitter Post Analysis")
    st.markdown("Analyze replies and engagement on a specific Twitter/X post")
    
    # Post URL input
    post_url = st.text_input(
        "Twitter/X Post URL:",
        placeholder="https://x.com/username/status/1234567890",
        help="Enter the full URL of the Twitter/X post"
    )
    
    # Number of replies to analyze
    reply_count = st.slider("Number of replies to analyze:", 1, 100, 50)
    
    if st.button("🔍 Scrape & Analyze Post Replies", type="primary", disabled=not post_url.strip()):
        tweet_id = extract_tweet_id(post_url)
        if tweet_id:
            scrape_post_replies(tweet_id, reply_count)
        else:
            st.error("Invalid Twitter/X post URL format")

async def scrape_user_tweets(username, tweet_count):
    """Scrape tweets from a specific user"""
    try:
        with st.spinner(f"Scraping {tweet_count} tweets from @{username}..."):
            api = API()
            
            # Get user info first
            user = await api.user_by_login(username)
            if not user:
                st.error(f"User @{username} not found or account is private")
                return
            
            st.info(f"Found user: @{user.username} ({user.displayname}) - {user.followersCount} followers")
            
            # Scrape user tweets
            tweets = await gather(api.user_tweets(user.id, limit=tweet_count))
            
            if not tweets:
                st.warning(f"No tweets found for @{username}")
                return
            
            # Convert tweets to Comment objects
            comments = []
            for i, tweet in enumerate(tweets):
                comment = Comment(
                    id=f"tweet_{tweet.id}",
                    text=tweet.rawContent,
                    author_id=str(tweet.user.id),
                    author_username=tweet.user.username,
                    author_bio=tweet.user.description or "",
                    timestamp=tweet.date,
                    metrics={
                        "likes": tweet.likeCount,
                        "retweets": tweet.retweetCount,
                        "replies": tweet.replyCount,
                        "views": tweet.viewCount or 0
                    },
                    author_followers=tweet.user.followersCount,
                    author_verified=tweet.user.verified
                )
                comments.append(comment)
            
            st.success(f"✅ Scraped {len(comments)} tweets from @{username}")
            
            # Show preview
            with st.expander("📄 Scraped Tweets Preview", expanded=False):
                for i, comment in enumerate(comments[:5], 1):
                    st.write(f"**{i}.** {comment.text[:200]}{'...' if len(comment.text) > 200 else ''}")
                    st.write(f"   💖 {comment.metrics['likes']} | 🔄 {comment.metrics['retweets']} | 💬 {comment.metrics['replies']}")
                    st.write("---")
            
            # Run analysis
            await run_analysis_on_comments(comments, f"user_@{username}")
            
    except Exception as e:
        st.error(f"Failed to scrape tweets from @{username}: {str(e)}")
        st.exception(e)

async def scrape_post_replies(tweet_id, reply_count):
    """Scrape replies from a specific tweet"""
    try:
        with st.spinner(f"Scraping {reply_count} replies from tweet {tweet_id}..."):
            api = API()
            
            # Get original tweet info
            original_tweet = await api.tweet_details(int(tweet_id))
            if not original_tweet:
                st.error(f"Tweet {tweet_id} not found or is not accessible")
                return
            
            st.info(f"Original tweet by @{original_tweet.user.username}: {original_tweet.rawContent[:100]}...")
            
            # Scrape replies
            replies = await gather(api.tweet_replies(int(tweet_id), limit=reply_count))
            
            if not replies:
                st.warning(f"No replies found for tweet {tweet_id}")
                return
            
            # Convert replies to Comment objects
            comments = []
            for i, reply in enumerate(replies):
                comment = Comment(
                    id=f"reply_{reply.id}",
                    text=reply.rawContent,
                    author_id=str(reply.user.id),
                    author_username=reply.user.username,
                    author_bio=reply.user.description or "",
                    timestamp=reply.date,
                    metrics={
                        "likes": reply.likeCount,
                        "retweets": reply.retweetCount,
                        "replies": reply.replyCount,
                        "views": reply.viewCount or 0
                    },
                    author_followers=reply.user.followersCount,
                    author_verified=reply.user.verified
                )
                comments.append(comment)
            
            st.success(f"✅ Scraped {len(comments)} replies from tweet {tweet_id}")
            
            # Show preview
            with st.expander("📄 Scraped Replies Preview", expanded=False):
                for i, comment in enumerate(comments[:5], 1):
                    st.write(f"**{i}.** @{comment.author_username}: {comment.text[:200]}{'...' if len(comment.text) > 200 else ''}")
                    st.write(f"   💖 {comment.metrics['likes']} | 🔄 {comment.metrics['retweets']} | 💬 {comment.metrics['replies']}")
                    st.write("---")
            
            # Run analysis
            await run_analysis_on_comments(comments, f"tweet_{tweet_id}")
            
    except Exception as e:
        st.error(f"Failed to scrape replies from tweet {tweet_id}: {str(e)}")
        st.exception(e)

def scrape_user_tweets(username, tweet_count):
    """Wrapper to run async scraping function"""
    import asyncio
    
    try:
        # Check if we're already in an event loop
        try:
            loop = asyncio.get_running_loop()
            # If we're in a loop, run in a thread pool
            import concurrent.futures
            import threading
            
            def run_async():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(scrape_user_tweets_async(username, tweet_count))
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async)
                future.result()
                
        except RuntimeError:
            # No event loop running, safe to use asyncio.run()
            asyncio.run(scrape_user_tweets_async(username, tweet_count))
            
    except Exception as e:
        st.error(f"Failed to scrape tweets for user @{username}: {str(e)}")
        st.exception(e)

def scrape_post_replies(tweet_id, reply_count):
    """Wrapper to run async scraping function"""
    import asyncio
    
    try:
        # Check if we're already in an event loop
        try:
            loop = asyncio.get_running_loop()
            # If we're in a loop, run in a thread pool
            import concurrent.futures
            import threading
            
            def run_async():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(scrape_post_replies_async(tweet_id, reply_count))
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async)
                future.result()
                
        except RuntimeError:
            # No event loop running, safe to use asyncio.run()
            asyncio.run(scrape_post_replies_async(tweet_id, reply_count))
            
    except Exception as e:
        st.error(f"Failed to scrape replies for tweet {tweet_id}: {str(e)}")
        st.exception(e)

async def scrape_user_tweets_async(username, tweet_count):
    """Async implementation of user tweet scraping"""
    try:
        from twscrape import API, gather
        
        st.info(f"🔍 Scraping tweets from @{username}...")
        
        # Initialize API
        api = API()
        
        # Get user tweets
        tweets = []
        async for tweet in api.user_tweets(username, limit=tweet_count):
            tweets.append(tweet)
        
        if not tweets:
            st.warning(f"No tweets found for user @{username}")
            return
        
        # Convert tweets to Comment objects
        comments = []
        for tweet in tweets:
            comment = Comment(
                id=str(tweet.id),
                author=tweet.user.username,
                text=tweet.rawContent,
                timestamp=tweet.date.isoformat() if tweet.date else datetime.now().isoformat(),
                likes=tweet.likeCount or 0,
                replies=tweet.replyCount or 0,
                retweets=tweet.retweetCount or 0
            )
            comments.append(comment)
        
        st.success(f"✅ Scraped {len(comments)} tweets from @{username}")
        
        # Run analysis
        await run_analysis_on_comments(comments, f"user_{username}")
        
    except Exception as e:
        st.error(f"Failed to scrape tweets from @{username}: {str(e)}")
        st.exception(e)

async def scrape_post_replies_async(tweet_id, reply_count):
    """Async implementation of post reply scraping"""
    try:
        from twscrape import API, gather
        
        st.info(f"🔍 Scraping replies from tweet {tweet_id}...")
        
        # Initialize API
        api = API()
        
        # Get tweet replies
        replies = []
        async for reply in api.tweet_replies(tweet_id, limit=reply_count):
            replies.append(reply)
        
        if not replies:
            st.warning(f"No replies found for tweet {tweet_id}")
            return
        
        # Convert replies to Comment objects
        comments = []
        for reply in replies:
            comment = Comment(
                id=str(reply.id),
                author=reply.user.username,
                text=reply.rawContent,
                timestamp=reply.date.isoformat() if reply.date else datetime.now().isoformat(),
                likes=reply.likeCount or 0,
                replies=reply.replyCount or 0,
                retweets=reply.retweetCount or 0
            )
            comments.append(comment)
        
        st.success(f"✅ Scraped {len(comments)} replies from tweet {tweet_id}")
        
        # Run analysis
        await run_analysis_on_comments(comments, f"post_{tweet_id}")
        
    except Exception as e:
        st.error(f"Failed to scrape replies from tweet {tweet_id}: {str(e)}")
        st.exception(e)

async def run_analysis_on_comments(comments, source_id):
    """Run the multi-agent analysis on scraped comments"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Initializing orchestrator...")
        orchestrator = SocialMediaOrchestrator(st.session_state.gemini_api_key)
        progress_bar.progress(0.2)
        
        status_text.text("Running multi-agent analysis...")
        post_id = f"twitter_analysis_{source_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = await orchestrator.analyze_post_comments(post_id, comments)
        progress_bar.progress(1.0)
        
        status_text.text("Analysis complete!")
        
        # Save results
        with open("analysis_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        st.success(f"✅ Analysis complete! Processed {len(comments)} comments.")
        st.balloons()
        
        # Show quick results
        with st.expander("📊 Quick Results Preview", expanded=True):
            show_quick_results(results)
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.exception(e)

def analyze_comments_from_text(comments_text):
    """Process comments and run analysis - kept for compatibility"""
    """Process comments and run analysis"""
    try:
        # Parse comments
        comment_lines = [line.strip() for line in comments_text.split('\n') if line.strip()]
        
        if not comment_lines:
            st.error("No valid comments found.")
            return
        
        # Create Comment objects
        comments = []
        for i, text in enumerate(comment_lines):
            comment = Comment(
                id=f"demo_{i+1}",
                text=text,
                author_id=f"user_{i+1}",
                author_username=f"user_{i+1}",
                author_bio=f"Demo user {i+1}",
                timestamp=datetime.now(),
                metrics={"likes": 0, "retweets": 0, "replies": 0},
                author_followers=1000,
                author_verified=False
            )
            comments.append(comment)
        
        # Show progress
        with st.spinner(f"Analyzing {len(comments)} comments..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Initializing orchestrator...")
            orchestrator = SocialMediaOrchestrator(st.session_state.gemini_api_key)
            progress_bar.progress(0.2)
            
            status_text.text("Running multi-agent analysis...")
            post_id = f"streamlit_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            results = asyncio.run(orchestrator.analyze_post_comments(post_id, comments))
            progress_bar.progress(1.0)
            
            status_text.text("Analysis complete!")
        
        # Save results
        with open("analysis_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        st.success(f"✅ Analysis complete! Processed {len(comments)} comments.")
        st.balloons()
        
        # Show quick results
        with st.expander("📊 Quick Results Preview", expanded=True):
            show_quick_results(results)
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.exception(e)

def show_quick_results(results):
    """Show condensed results preview"""
    summary = results.get("summary", {})
    risk_assessment = results.get("risk_assessment", {})
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Comments", summary.get("total_comments", 0))
    with col2:
        risk = risk_assessment.get("overall_risk", "unknown")
        risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        st.metric("Risk Level", f"{risk_colors.get(risk, '⚪')} {risk.upper()}")
    with col3:
        st.metric("Flagged", risk_assessment.get("flagged_comments", 0))
    with col4:
        avg_toxicity = summary.get("average_toxicity", 0)
        st.metric("Avg Toxicity", f"{avg_toxicity:.2f}")

def show_dashboard_page():
    """Comprehensive results dashboard"""
    st.title("📊 Analysis Dashboard")
    
    if not os.path.exists("analysis_results.json"):
        st.info("No analysis results found. Please run an analysis first.")
        return
    
    try:
        with open("analysis_results.json", "r") as f:
            results = json.load(f)
        
        # Main metrics
        show_main_metrics(results)
        st.markdown("---")
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            show_sentiment_chart(results)
        
        with col2:
            show_risk_analysis(results)
        
        st.markdown("---")
        
        # Detailed analysis
        show_detailed_analysis(results)
        
    except Exception as e:
        st.error(f"Error loading results: {str(e)}")

def show_main_metrics(results):
    """Display main dashboard metrics"""
    summary = results.get("summary", {})
    risk_assessment = results.get("risk_assessment", {})
    
    st.subheader("📈 Overview Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Comments", summary.get("total_comments", 0))
    
    with col2:
        risk = risk_assessment.get("overall_risk", "unknown")
        risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        st.metric("Risk Level", f"{risk_colors.get(risk, '⚪')} {risk.upper()}")
    
    with col3:
        flagged = risk_assessment.get("flagged_comments", 0)
        total = summary.get("total_comments", 1)
        flagged_pct = (flagged / total) * 100 if total > 0 else 0
        st.metric("Flagged Comments", f"{flagged} ({flagged_pct:.1f}%)")
    
    with col4:
        avg_toxicity = summary.get("average_toxicity", 0)
        st.metric("Avg Toxicity", f"{avg_toxicity:.3f}")
    
    with col5:
        bias_count = len(results.get("bias_analyses", []))
        st.metric("Bias Analyses", bias_count)

def show_sentiment_chart(results):
    """Display sentiment distribution chart"""
    st.subheader("💭 Sentiment Distribution")
    
    sentiment_data = results.get("summary", {}).get("sentiment_distribution", {})
    
    if sentiment_data and any(sentiment_data.values()):
        # Create pie chart
        fig = px.pie(
            values=list(sentiment_data.values()),
            names=list(sentiment_data.keys()),
            title="Comment Sentiment",
            color_discrete_map={
                'positive': '#10b981',
                'negative': '#ef4444', 
                'neutral': '#6b7280'
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sentiment data available")

def show_risk_analysis(results):
    """Display risk analysis"""
    st.subheader("⚠️ Risk Assessment")
    
    risk_assessment = results.get("risk_assessment", {})
    
    # Risk level indicator
    risk = risk_assessment.get("overall_risk", "unknown")
    risk_colors = {"low": "#10b981", "medium": "#f59e0b", "high": "#ef4444"}
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = {"low": 25, "medium": 60, "high": 90}.get(risk, 0),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Level"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': risk_colors.get(risk, "#6b7280")},
            'steps': [
                {'range': [0, 33], 'color': "#dcfce7"},
                {'range': [33, 66], 'color': "#fef3c7"},
                {'range': [66, 100], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    recommendations = risk_assessment.get("recommendations", [])
    if recommendations:
        st.markdown("**Recommendations:**")
        for rec in recommendations:
            st.write(f"• {rec}")

def show_detailed_analysis(results):
    """Show detailed comment analysis"""
    st.subheader("🔍 Detailed Analysis")
    
    # Comment classifications
    classifications = results.get("classifications", [])
    if classifications:
        with st.expander("📋 Comment Classifications", expanded=False):
            df = pd.DataFrame(classifications)
            st.dataframe(df, use_container_width=True)
    
    # Bias analyses
    bias_analyses = results.get("bias_analyses", [])
    if bias_analyses:
        with st.expander("🚨 Bias Analysis Results", expanded=True):
            for i, bias in enumerate(bias_analyses, 1):
                st.markdown(f"**Comment {i}:**")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Text:** {bias.get('comment_text', 'N/A')}")
                    st.write(f"**Explanation:** {bias.get('explanation', 'N/A')}")
                
                with col2:
                    st.metric("Bias Score", f"{bias.get('bias_score', 0):.2f}")
                    st.metric("Risk Level", bias.get('risk_level', 'Unknown').upper())
                
                if bias.get('bias_signals'):
                    signals = bias['bias_signals']
                    st.write("**Bias Signals:**")
                    for signal, score in signals.items():
                        st.write(f"• {signal.replace('_', ' ').title()}: {score:.2f}")
                
                st.markdown("---")
    
    # Summary bullets
    bullets = results.get("summary", {}).get("summary_bullets", [])
    if bullets:
        with st.expander("📝 Summary Points", expanded=False):
            for bullet in bullets:
                st.write(f"• {bullet}")

def show_documentation_page():
    """Documentation and help"""
    st.title("📚 Documentation")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Overview", "🔧 How to Use", "📊 Understanding Results"])
    
    with tab1:
        st.markdown("""
        ## Social Media Analysis System
        
        This application uses advanced AI agents to analyze social media comments for:
        
        - **Sentiment Analysis**: Positive, negative, or neutral sentiment
        - **Bias Detection**: Commercial bias, promotional content, authenticity
        - **Toxicity Scoring**: Harmful or offensive content detection
        - **Risk Assessment**: Overall content risk evaluation
        
        ### Multi-Agent Architecture
        
        1. **Main Classifier**: Initial comment classification and toxicity detection
        2. **Summary Agent**: Maintains running statistics and generates insights
        3. **Bias Detection Agent**: Deep analysis of flagged suspicious content
        4. **Orchestrator**: Coordinates all agents and manages the pipeline
        """)
    
    with tab2:
        st.markdown("""
        ## How to Use
        
        ### 1. Setup
        - Enter your Gemini API key in the sidebar
        - The key is stored securely in your session
        
        ### 2. Input Methods
        - **Manual Input**: Type or paste comments directly
        - **Demo Scenarios**: Try pre-built examples
        - **CSV Upload**: Bulk analyze from spreadsheet
        
        ### 3. Analysis Process
        - Comments are processed through multiple AI agents
        - Results are saved automatically
        - View detailed analysis in the Dashboard
        
        ### 4. Interpreting Results
        - Check the Dashboard for comprehensive visualizations
        - Review flagged comments for potential bias
        - Use recommendations for content moderation
        """)
    
    with tab3:
        st.markdown("""
        ## Understanding Results
        
        ### Risk Levels
        - **🟢 Low**: Normal, authentic engagement
        - **🟡 Medium**: Some suspicious patterns detected
        - **🔴 High**: Strong indicators of bias or manipulation
        
        ### Bias Signals
        - **Brand Affinity**: Commercial relationships or partnerships
        - **Promotional Content**: Marketing language, discount codes
        - **Account Credibility**: Profile authenticity indicators
        
        ### Classifications
        - **Factual**: Objective, informational content
        - **Opinionated**: Personal views and subjective content
        - **Polarized**: Extreme or divisive opinions
        
        ### Toxicity Scores
        - **0.0-0.3**: Clean, appropriate content
        - **0.3-0.7**: Moderately concerning language
        - **0.7-1.0**: High toxicity, requires attention
        """)

if __name__ == "__main__":
    main()