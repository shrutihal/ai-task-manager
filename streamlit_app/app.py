import streamlit as st
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Load model and tokenizer from local storage
model_path = "./local_model"  # Ensure this directory contains the downloaded model
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize classifier
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)
 
# Define priority labels
priority_labels = [
    "Urgent & Important",       # Highest Priority (Do First)
    "Urgent but Not Important", # Delegate if possible
    "Important but Not Urgent", # Schedule for later
    "Low Priority"              # Least Important
]

# Streamlit UI
st.title("📌 AI Task Manager")
st.write("Enter multiple tasks separated by commas. The AI will prioritize them.")

# Disclosure Section
st.markdown("---")
st.warning("⚠️ **Disclaimer:** This AI-generated task prioritization is a suggestion and may not reflect personal preferences or real-world urgency. Please use personal judgment when managing tasks.")

# Priority Levels - Placed Above Input Field
st.subheader("📌 How Tasks Are Prioritized")
st.markdown("""
- **Urgent & Important** → Must be done immediately! 
- **Urgent but Not Important** → Should be done soon or delegated. 
- **Important but Not Urgent** → Can be scheduled for later. 
- **Low Priority** → Leisure or optional tasks. 
""")

# User Input
task_input = st.text_area("📝 Enter your tasks", placeholder="E.g., I need to file my taxes, call doctor, get my car checked, catch up on Netflix shows")

if st.button("Classify & Prioritize Tasks"):
    if task_input:
       
        # Split tasks by commas
        tasks = [task.strip() for task in task_input.split(",") if task.strip()]
        task_priorities = []
        
        # Classify each task with proper context
        for task in tasks:
            result = classifier(
                task,
                priority_labels,
                multi_label=False  # Multi-label classification for better results
            )
            priority = result["labels"][0]
            
            # Adjust priority for clear non-essential activities, testing.
            # if "Netflix" in task.lower() or "watch" in task.lower() or "game" in task.lower():
            #     priority = "Low Priority"
            
            task_priorities.append((task, priority))
        
        # Sort tasks by priority
        
        priority_order = {
            "Urgent & Important": 1,
            "Urgent but Not Important": 2,
            "Important but Not Urgent": 3,
            "Low Priority": 4
        }
        sorted_tasks = sorted(task_priorities, key=lambda x: priority_order[x[1]])
        
        # Display Prioritized Tasks
        st.subheader("📌 Prioritized Task List")
        for i, (task, priority) in enumerate(sorted_tasks, start=1):
            if priority == "Urgent & Important":
                st.markdown(f"<h3 style='color: red; font-weight: bold;'>{i}. {task} → {priority}</h3>", unsafe_allow_html=True)
            else:
                st.write(f"**{i}. {task}** → _{priority}_")
    else:
        st.warning("Please enter at least one task.")
