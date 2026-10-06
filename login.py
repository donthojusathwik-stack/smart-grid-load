import streamlit as st
from auth import login_user

def show_login():
    """Display login page"""
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: inherit;
            border: none;
            padding: 12px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 400px;
            margin: 50px auto;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        # Logo and title
        st.markdown("<h1 style='text-align: center; color: #667eea;'>⚡</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #333;'>Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Energy Consumption Predictor</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            remember = st.checkbox("Remember me")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Login")
            with col_btn2:
                if st.form_submit_button("Register"):
                    st.session_state.page = "register"
                    st.rerun()
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields!")
                else:
                    success, result = login_user(username, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = result
                        st.session_state.page = "app"
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(result)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("<p class='contrast-box' style='text-align: center; margin-top: 20px; font-size: 12px;'>© 2025 Energy Predictor. All rights reserved.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_login()