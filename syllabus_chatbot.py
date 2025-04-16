import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.text_processing import extract_weekly_content
from utils.vector_storage import store_embeddings
from utils.chatbot import create_chatbot, chat_with_bot

# Function to process user queries and return relevant syllabus content
def process_query(query, weekly_content):
    query = query.lower()  # Convert query to lowercase for easier matching
    
    if "week" in query:
        # Extract the week number from the query (e.g., "Week 4")
        week_number = query.split("week")[-1].strip()  # Get the number after 'Week'
        
        # Search for the requested week in the weekly content
        week_info = weekly_content.get(f"Week {week_number}", None)
        if week_info:
            return f"In Week {week_number}, the following topics are covered: {', '.join(week_info['readings'])}. Assignments: {', '.join(week_info['assignments'])}."
        else:
            return f"Sorry, I couldn't find details for Week {week_number}."
    
    elif "midterm" in query:
        # Look for any week that has a midterm
        for week, info in weekly_content.items():
            if info.get("midterm"):
                return f"The midterm is scheduled for {info['midterm']}."
        return "Sorry, I couldn't find the midterm details."

    elif "assignment" in query:
        # Look for assignments across weeks
        for week, info in weekly_content.items():
            if info["assignments"]:
                return f"Assignments for {week}: {', '.join(info['assignments'])}"
        return "Sorry, I couldn't find any assignments."
    
    else:
        return "Sorry, I didn't understand the question. Please ask about a specific week, assignment, or midterm."

def main():
    st.title("University Course Syllabus Chatbot")

    # Upload PDF
    uploaded_file = st.file_uploader("Upload your syllabus PDF", type="pdf")
    
    if uploaded_file:
        # Step 1: Extract text from PDF
        syllabus_text = extract_text_from_pdf(uploaded_file)

        # Debug: Display the first 500 characters of the extracted text
        st.write(syllabus_text[:500])  # Display only the first 500 characters for verification
        print(f"Extracted syllabus text: {syllabus_text[:500]}")  # Print for debugging
        
        # Step 2: Process the weekly content
        weekly_content = extract_weekly_content(syllabus_text)

        # Debug: Print the weekly content to the console for inspection
        print(f"Extracted weekly content: {weekly_content}")

        # Step 3: Store embeddings and create the chatbot
        if weekly_content:  # Ensure there is weekly content before processing
            index, texts = store_embeddings(weekly_content)
            chatbot = create_chatbot(index, texts)

            # Step 4: Create a simple chat interface
            user_input = st.text_input("Ask the chatbot a question about the syllabus:")

            if user_input:
                # Process the user's question and generate the answer
                answer = process_query(user_input, weekly_content)
                st.write(answer)
        else:
            st.write("No weekly content extracted. Please check the syllabus structure.")

if __name__ == "__main__":
    main()
