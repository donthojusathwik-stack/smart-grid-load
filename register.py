import streamlit as st
import re
from auth import register_user

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain lowercase letters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain uppercase letters"
    if not re.search(r"\d", password):
        return False, "Password must contain numbers"
    return True, "Strong password"

def show_register():
    """Display registration page"""
    
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
        .register-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 450px;
            margin: 30px auto;
        }
        .password-strength {
            padding: 8px;
            border-radius: 5px;
            margin-top: 5px;
            font-size: 12px;
        }
        .strength-weak {
            background: #fee;
            color: #c33;
        }
        .strength-medium {
            background: #fef3cd;
            color: #856404;
        }
        .strength-strong {
            background: #d4edda;
            color: #155724;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='register-container'>", unsafe_allow_html=True)
        
        # Logo and title
        st.markdown("<h1 style='text-align: center; color: #667eea;'>⚡</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #333;'>Create Account</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Join Energy Predictor today</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Registration form
        with st.form("register_form"):
            username = st.text_input("Username", placeholder="Choose a username (min 3 characters)")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            # Password strength indicator
            if password:
                is_valid, message = validate_password(password)
                if is_valid:
                    st.markdown(f"<div class='password-strength strength-strong'>✓ {message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='password-strength strength-weak'>✗ {message}</div>", unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Register")
            with col_btn2:
                if st.form_submit_button("Back to Login"):
                    st.session_state.page = "login"
                    st.rerun()
            
            if submit:
                # Validation
                if not username or not email or not password or not confirm_password:
                    st.error("Please fill in all fields!")
                elif len(username) < 3:
                    st.error("Username must be at least 3 characters long!")
                elif not validate_email(email):
                    st.error("Please enter a valid email address!")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    is_valid, message = validate_password(password)
                    if not is_valid:
                        st.error(message)
                    else:
                        # Register user
                        success, result = register_user(username, email, password)
                        
                        if success:
                            st.success("✓ " + result + " Please login to continue.")
                            st.balloons()
                            # Redirect to login after 2 seconds
                            import time
                            time.sleep(2)
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error(result)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("<p class='contrast-box' style='text-align: center; margin-top: 20px; font-size: 12px;'>© 2024 Energy Predictor. All rights reserved.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_register()