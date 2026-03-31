import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.chat_logic import ChatLogic
from app.admin_dashboard import AdminDashboard
from app.config import Config
from app.booking_form import render_booking_form, process_booking_confirmation
from app.booking_success import render_booking_success

def main():
    st.set_page_config(
        page_title="🏨 AI Hotel Booking Assistant",
        page_icon="🏨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'chat_logic' not in st.session_state:
        st.session_state.chat_logic = ChatLogic()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "hotel_booking"
    if 'selected_hotel' not in st.session_state:
        st.session_state.selected_hotel = None
    if 'booking_step' not in st.session_state:
        st.session_state.booking_step = 1
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🏨 AI Hotel Booking Assistant")
        st.markdown("---")
        
        if st.button("🏨 Hotel Booking", key="hotel_booking_btn", use_container_width=True):
            st.session_state.current_page = "hotel_booking"
        
        if st.button("💬 Smart Chat", key="smart_chat_btn", use_container_width=True):
            st.session_state.current_page = "smart_chat"
        
        if st.button("📊 Admin Dashboard", key="admin_btn", use_container_width=True):
            st.session_state.current_page = "admin"
        
        st.markdown("---")
        
        # Quick Actions
        st.subheader("🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏖️ Beach Resorts", key="beach_btn", use_container_width=True):
                st.session_state.current_page = "beach_resorts"
        
        with col2:
            if st.button("🏔️ Budget Hotels", key="budget_btn", use_container_width=True):
                st.session_state.current_page = "budget_hotels"
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🌟 Luxury Hotels", key="luxury_btn", use_container_width=True):
                st.session_state.current_page = "luxury_hotels"
        
        with col4:
            if st.button("🏔️ Hill Stations", key="hill_btn", use_container_width=True):
                st.session_state.current_page = "hill_stations"
        
        st.markdown("---")
        
        # Smart Suggestions
        st.subheader("💡 Smart Suggestions")
        
        st.markdown("**Nearby Cities**")
        cities = ["Panjim", "Margao", "Vasco"]
        for city in cities:
            if st.button(f"📍 {city}", key=f"city_{city}", use_container_width=True):
                st.session_state.selected_city = city
                st.session_state.current_page = "city_hotels"
        
        st.markdown("**Alternative Amenities**")
        amenities = ["WiFi", "Pool", "Spa", "AC", "Parking", "Breakfast"]
        selected_amenities = st.multiselect("Select Amenities:", amenities, key="amenities")
        
        if selected_amenities:
            st.success(f"✅ Selected amenities: {', '.join(selected_amenities)}")
    
    # Route to appropriate page
    if st.session_state.current_page == "hotel_booking":
        render_hotel_booking_interface()
    elif st.session_state.current_page == "smart_chat":
        render_smart_chat_interface()
    elif st.session_state.current_page == "admin":
        render_admin_interface()
    elif st.session_state.current_page == "beach_resorts":
        render_beach_resorts()
    elif st.session_state.current_page == "budget_hotels":
        render_budget_hotels()
    elif st.session_state.current_page == "luxury_hotels":
        render_luxury_hotels()
    elif st.session_state.current_page == "hill_stations":
        render_hill_stations()
    elif st.session_state.current_page == "city_hotels":
        render_city_hotels()
    elif st.session_state.current_page == "booking_form":
        render_booking_form()
    elif st.session_state.current_page == "booking_success":
        render_booking_success()

def render_hotel_booking_interface():
    """Render the main hotel booking interface"""
    st.title("🏨 Find and book the perfect hotel with AI-powered intelligence")
    
    # Search section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Search Hotels")
        
        # Location input
        location = st.text_input("📍 Where are you looking for hotels?", 
                            placeholder="Enter city or area...", 
                            key="location")
        
        # Date range
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            check_in = st.date_input("📅 Check-in Date", key="check_in")
        with col_date2:
            check_out = st.date_input("📅 Check-out Date", key="check_out")
        
        # Guests and rooms
        col_guest1, col_guest2, col_room = st.columns(3)
        with col_guest1:
            adults = st.number_input("👥 Adults", min_value=1, max_value=10, value=1, key="adults")
        with col_guest2:
            children = st.number_input("👶 Children", min_value=0, max_value=10, value=0, key="children")
        with col_room:
            rooms = st.number_input("🛏️ Rooms", min_value=1, max_value=5, value=1, key="rooms")
        
        # Budget range
        budget_min = st.number_input("💰 Min Budget (₹)", min_value=0, value=1000, key="budget_min")
        budget_max = st.number_input("💰 Max Budget (₹)", min_value=0, value=10000, key="budget_max")
        
        # Search button
        if st.button("🔍 Search Hotels", key="search_hotels", use_container_width=True):
            st.session_state.search_params = {
                'location': location,
                'check_in': check_in,
                'check_out': check_out,
                'adults': adults,
                'children': children,
                'rooms': rooms,
                'budget_min': budget_min,
                'budget_max': budget_max
            }
            st.success("🔍 Searching for the best hotels...")
            st.rerun()
    
    with col2:
        st.subheader("🤖 AI Assistant")
        
        # Chat-like interface for hotel recommendations
        with st.container(height=400):
            st.markdown("### 💬 Ask me anything about hotels!")
            
            # Quick question buttons
            questions = [
                "What are the best beach resorts in Goa?",
                "Find budget hotels in Delhi under ₹3000",
                "Show luxury hotels with spa in Mumbai",
                "Recommend hill stations near Delhi",
                "What amenities do 5-star hotels offer?"
            ]
            
            for i, question in enumerate(questions):
                if st.button(f"💡 {question}", key=f"question_{i}", use_container_width=True):
                    st.session_state.chat_logic.process_message(question)
                    st.rerun()
        
        # Custom question input
        custom_question = st.text_input("Or type your own question:", 
                                   placeholder="What kind of hotel are you looking for?",
                                   key="custom_question")
        
        if st.button("🤔 Ask AI", key="ask_ai"):
            if custom_question:
                response = st.session_state.chat_logic.process_message(custom_question)
                st.session_state.ai_response = response
                st.rerun()
        
        # Display AI response
        if 'ai_response' in st.session_state:
            with st.chat_message("assistant"):
                st.markdown(st.session_state.ai_response)
    
    # Display search results if available
    if 'search_params' in st.session_state:
        render_hotel_search_results()

def render_hotel_search_results():
    """Render hotel search results"""
    st.subheader("🏨 Available Hotels")
    
    # Mock hotel data (in real app, this would come from API)
    hotels = [
        {
            "name": "Beach Paradise Resort - Goa",
            "price": 6500,
            "rating": 4.5,
            "amenities": ["WiFi", "Pool", "Breakfast", "AC", "Parking", "Spa", "Beach Access"],
            "image": "https://via.placeholder.com/300x200.png?text=Beach+Resort",
            "description": "Luxurious beachfront property with stunning ocean views and world-class amenities"
        },
        {
            "name": "Goa Village Retreat",
            "price": 3800,
            "rating": 4.0,
            "amenities": ["WiFi", "Pool", "Breakfast", "AC"],
            "image": "https://via.placeholder.com/300x200.png?text=Goa+Village",
            "description": "Cozy retreat nestled in lush greenery with traditional Goan hospitality"
        },
        {
            "name": "Coastal Haven Hotel",
            "price": 5200,
            "rating": 4.2,
            "amenities": ["WiFi", "Pool", "AC", "Restaurant"],
            "image": "https://via.placeholder.com/300x200.png?text=Coastal+Haven",
            "description": "Modern beach hotel with excellent service and stunning sea views"
        }
    ]
    
    # Filter hotels based on search criteria
    filtered_hotels = filter_hotels(hotels, st.session_state.search_params)
    
    # Display hotels in a grid
    cols = st.columns(3)
    for i, hotel in enumerate(filtered_hotels):
        with cols[i % 3]:
            render_hotel_card(hotel, i)

def render_hotel_card(hotel, index):
    """Render individual hotel card"""
    with st.container():
        # Hotel image and basic info
        st.image(hotel["image"], width=300)
        st.markdown(f"### {hotel['name']}")
        
        # Rating and price
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"⭐ {hotel['rating']}/5")
        with col2:
            st.markdown(f"💰 ₹{hotel['price']}/night")
        
        # Amenities
        st.markdown("**Amenities:**")
        amenity_cols = st.columns(4)
        for i, amenity in enumerate(hotel['amenities'][:4]):
            with amenity_cols[i]:
                st.markdown(f"✅ {amenity}")
        
        # Description
        with st.expander("📝 About this hotel"):
            st.markdown(hotel['description'])
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📖 More Details", key=f"details_{index}"):
                st.session_state.selected_hotel = hotel
                st.session_state.current_page = "hotel_details"
                st.rerun()
        
        with col2:
            if st.button("❤️ Save", key=f"save_{index}"):
                st.success(f"❤️ {hotel['name']} saved to favorites!")
        
        with col3:
            if st.button("🏨 Book Now", key=f"book_{index}"):
                st.session_state.selected_hotel = hotel
                st.session_state.current_page = "booking_form"
                st.rerun()
        
        st.markdown("---")

def filter_hotels(hotels, search_params):
    """Filter hotels based on search criteria"""
    filtered = hotels.copy()
    
    # Filter by budget
    if search_params.get('budget_min'):
        filtered = [h for h in filtered if h['price'] >= search_params['budget_min']]
    if search_params.get('budget_max'):
        filtered = [h for h in filtered if h['price'] <= search_params['budget_max']]
    
    # Filter by rating (minimum 4.0)
    filtered = [h for h in filtered if h['rating'] >= 4.0]
    
    return filtered

def render_beach_resorts():
    """Render beach resorts page"""
    st.title("🏖️ Beach Resorts in Goa")
    
    resorts = [
        {
            "name": "Beach Paradise Resort - Goa",
            "price": 6500,
            "rating": 4.5,
            "amenities": ["WiFi", "Pool", "Breakfast", "AC", "Parking", "Spa", "Beach Access"]
        },
        {
            "name": "Goa Village Retreat",
            "price": 3800,
            "rating": 4.0,
            "amenities": ["WiFi", "Pool", "Breakfast", "AC"]
        }
    ]
    
    for resort in resorts:
        render_hotel_card(resort, 0)

def render_budget_hotels():
    """Render budget hotels page"""
    st.title("🏔️ Budget Hotels in Delhi")
    
    # Similar structure to render_hotel_card but with budget hotels
    st.info("🏔️ Budget hotels coming soon...")

def render_luxury_hotels():
    """Render luxury hotels page"""
    st.title("🌟 Luxury Hotels in Mumbai")
    
    # Similar structure with luxury hotels
    st.info("🌟 Luxury hotels coming soon...")

def render_hill_stations():
    """Render hill stations page"""
    st.title("🏔️ Hill Stations in Manali")
    
    # Similar structure with hill station hotels
    st.info("🏔️ Hill station hotels coming soon...")

def render_city_hotels():
    """Render city-specific hotels"""
    city = st.session_state.get('selected_city', 'Panjim')
    st.title(f"📍 Hotels in {city}")
    
    st.info(f"📍 Hotels in {city} coming soon...")

def render_smart_chat_interface():
    """Render enhanced smart chat interface"""
    st.title("💬 Smart AI Assistant")
    
    # PDF upload section
    with st.expander("📄 Upload PDF Documents", expanded=False):
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type="pdf",
            accept_multiple_files=True,
            key="pdf_uploader"
        )
        
        if uploaded_files:
            if st.button("📥 Process PDFs", key="process_pdfs"):
                with st.spinner("Processing PDFs..."):
                    try:
                        for file in uploaded_files:
                            st.session_state.chat_logic.process_pdf(file)
                        st.success(f"Successfully processed {len(uploaded_files)} PDF(s)!")
                    except Exception as e:
                        st.error(f"Error processing PDFs: {str(e)}")
    
    # Chat interface
    st.markdown("---")
    st.subheader("💬 Chat with AI Assistant")
    
    # Display chat messages
    for message in st.session_state.chat_logic.get_chat_history():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Enhanced chat input with quick options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Quick action buttons
        st.markdown("**Quick Actions:**")
        
        quick_actions = [
            ("🏨 Book Hotel", "I want to book a hotel"),
            ("📄 Ask About Services", "What services do you offer?"),
            ("📊 Check Availability", "Check hotel availability for next weekend"),
            ("💰 Price Information", "What are your room rates?"),
            ("📍 Location Info", "Where are your hotels located?"),
            ("🏖️ Amenities", "What amenities do you provide?"),
            ("❓ Help", "help")
        ]
        
        action_cols = st.columns(3)
        for i, (label, message) in enumerate(quick_actions):
            with action_cols[i % 3]:
                if st.button(label, key=f"action_{i}"):
                    st.session_state.quick_message = message
                    st.rerun()
    
    with col2:
        st.markdown("**Or type:**")
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chat_logic.process_message(prompt)
                        st.markdown(response)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Process quick action if selected
        if 'quick_message' in st.session_state:
            prompt = st.session_state.quick_message
            del st.session_state.quick_message
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chat_logic.process_message(prompt)
                        st.markdown(response)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            st.rerun()

def render_admin_interface():
    """Render admin dashboard"""
    dashboard = AdminDashboard()
    dashboard.render()

if __name__ == "__main__":
    main()
