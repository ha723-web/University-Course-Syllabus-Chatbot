
# 🎓 **University Course Syllabus Chatbot** 🤖

This project implements a smart chatbot that reads a university course syllabus from a PDF 📄 and allows students to easily ask questions about weekly topics, assignments 📅, and exam schedules 📚.

## 🛠️ **Tools Used**:
- 🐍 **Python**
- 📄 **PyMuPDF** (for reading PDFs)
- 🧠 **LangChain** (for chatbot creation)
- 🗃️ **FAISS** (for vector storage)
- 💬 **OpenAI API**

## 🚀 **How to Run**:

1. **Install the Required Dependencies**:
   Before getting started, make sure you have Python 3.7 or above installed. Then, set up a virtual environment and install the required libraries by running:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   pip install -r requirements.txt
   ```
   This will ensure all necessary libraries are installed for the project to run smoothly. 🔧✨

2. **Prepare Your PDF Syllabus** 📄:
   Find or upload a university course syllabus in PDF format that you'll feed into the chatbot. This will be the source of all course details like topics, assignments, exams, etc.

3. **Extract Text from the PDF** 📝:
   The `PyMuPDF` library (imported as `fitz`) will be used to extract the syllabus text. This allows you to access all course content.
   Example usage:
   ```python
   syllabus_text = extract_text_from_pdf("path_to_syllabus.pdf")
   ```

4. **Process Weekly Content** 📆:
   The extracted syllabus text will be processed to identify weekly sections, assignments, and exam schedules. The `extract_weekly_content()` function will structure this data neatly for further use.
   Example usage:
   ```python
   weekly_content = extract_weekly_content(syllabus_text)
   ```

5. **Store Data for Fast Search** 🔍:
   To make the chatbot efficient in answering questions, we'll store the processed content as **embeddings** using **FAISS**. This makes searching through the syllabus lightning fast.
   Example usage:
   ```python
   index, texts = store_embeddings(weekly_content)
   ```

6. **Set Up the Chatbot** 🗣️:
   The core of this project! The `LangChain` framework will be used to create a chatbot that can answer student queries. The chatbot uses the **FAISS index** for fast information retrieval.
   Example usage:
   ```python
   chatbot = create_chatbot(index, texts)
   ```

7. **Run the Chatbot with Streamlit** 🌐:
   You can start the chatbot and interact with it through a simple **web app** created using Streamlit. Students can upload their syllabus PDF, and the chatbot will answer any questions they have about the course.
   
   Example usage:
   ```python
   import streamlit as st
   from utils.chatbot import chat_with_bot

   def main():
       st.title("🎓 University Course Syllabus Chatbot 🤖")

       # Upload PDF
       uploaded_file = st.file_uploader("Upload your syllabus PDF 📄", type="pdf")
       
       if uploaded_file:
           syllabus_text = extract_text_from_pdf(uploaded_file)
           weekly_content = extract_weekly_content(syllabus_text)
           index, texts = store_embeddings(weekly_content)
           chatbot = create_chatbot(index, texts)

           # Ask questions
           query = st.text_input("Ask the chatbot about your syllabus 🤔:")
           if query:
               answer = chat_with_bot(query, chatbot)
               st.write(f"Answer: {answer} 🧠")

   if __name__ == "__main__":
       main()
   ```

8. **Start the App** 🚀:
   Once everything is set up, you can run the Streamlit web app with the following command:
   ```bash
   streamlit run app.py
   ```
   Your chatbot is now live! 🦾

9. **Test the Chatbot** 🧑‍🎓:
   Visit the local URL provided by Streamlit (usually `http://localhost:8501/`) and try uploading a syllabus PDF. Ask the chatbot any questions about the course, and it will provide helpful answers! 🎉

---

### 🌟 **Additional Features to Consider**:
- **Enhancing the Chatbot's Accuracy**: 🤖💡 You can fine-tune the AI model with additional course materials and student feedback for even more accurate responses.
- **Multi-file Support**: 📂 Allow students to upload multiple syllabus PDFs or course materials, enabling the chatbot to answer questions across different documents.
- **Dynamic Query Expansion**: 🔄 Automatically enhance user queries by recognizing synonyms or related terms in the syllabus for broader query coverage.
