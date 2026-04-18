import streamlit as st
import json
from pathlib import Path

# --- HELPER FUNCTIONS ---

def load_json(path):
    """Loads JSON data safely, handling BOM and missing files."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig").strip()
        return json.loads(text) if text else {}
    except (FileNotFoundError, ValueError):
        return {}

def save_json(path, data):
    """Saves data to a JSON file with proper formatting."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def update_task_flow(tasks):
    """Orchestrates task status based on dependencies."""
    for i, task in enumerate(tasks):
        if i == 0:
            continue
        prev_task = tasks[i - 1]
        if task["dependency"] == "After previous task":
            if prev_task["status"] == "Done" and task["status"] == "Pending":
                task["status"] = "Active"
            elif prev_task["status"] == "Delayed":
                task["status"] = "Blocked"
    return tasks

def get_providers_by_category(providers, category, active_only=False, collab_only=False):
    filtered = [p for p in providers if p["category"] == category]
    if active_only:
        filtered = [p for p in filtered if p["active"]]
    if collab_only:
        filtered = [p for p in filtered if p["collab_ready"]]
    return filtered

def suggest_backup(providers, category, current_provider):
    options = [
        p for p in providers
        if p["category"] == category and p["name"] != current_provider and p["available"]
    ]
    return options[0]["name"] if options else "No backup available"

def can_share_data(master_permission, task_permission):
    return master_permission and task_permission

# --- APP CONFIGURATION ---

st.set_page_config(page_title="Life Canvas", layout="wide")

# Ensure paths match your folder structure
customer_path = "data/customer_profile.json"
providers_path = "data/providers.json"
tasks_path = "data/tasks.json"

# Initialize Session State
if "customer" not in st.session_state:
    st.session_state.customer = load_json(customer_path)
if "tasks" not in st.session_state:
    st.session_state.tasks = load_json(tasks_path)
if "providers" not in st.session_state:
    st.session_state.providers = load_json(providers_path)

st.title("Life Canvas")
st.caption("Your Data. Your Money. Your Terms.")

left, center, right = st.columns([1.1, 1.4, 1.1])

# --- LEFT COLUMN: CUSTOMER VAULT ---
with left:
    st.subheader("Customer Registration Vault")
    with st.form("customer_form"):
        # Use .get() to avoid KeyErrors if JSON fields are missing
        name = st.text_input("Full Name", st.session_state.customer.get("name", ""))
        phone = st.text_input("Phone", st.session_state.customer.get("phone", ""))
        email = st.text_input("Email", st.session_state.customer.get("email", ""))
        address = st.text_input("Address", st.session_state.customer.get("address", ""))
        
        food_options = ["Veg", "Non-Veg", "Vegan", "Jain"]
        food_choice = st.selectbox("Food Choice", food_options, 
                                  index=food_options.index(st.session_state.customer.get("food_choice", "Veg")))
        
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state.customer.update({
                "name": name, "phone": phone, "email": email, 
                "address": address, "food_choice": food_choice
            })
            save_json(customer_path, st.session_state.customer)
            st.success("Profile saved successfully!")

    master_permission = st.toggle("Allow sharing selected profile fields", value=True)

# --- CENTER COLUMN: TASK ORCHESTRATOR ---
with center:
    st.subheader("Task Flow")
    
    # Preset Automation Buttons
    if st.button("Travel + Food Plan", use_container_width=True):
        st.session_state.tasks = [
            {"task_name": "Book Train", "category": "Travel", "provider": "RailYatri Mock", "dependency": "Independent", "status": "Done", "share_data": True},
            {"task_name": "Order Food", "category": "Food Delivery", "provider": "Zomato Mock", "dependency": "After previous task", "status": "Pending", "share_data": True}
        ]
        save_json(tasks_path, st.session_state.tasks)
        st.rerun()

    # Update task logic (Pending -> Active)
    st.session_state.tasks = update_task_flow(st.session_state.tasks)

    for i, task in enumerate(st.session_state.tasks):
        with st.expander(f"{task['task_name']} ({task['status']})", expanded=(task['status'] == "Active")):
            st.write(f"Provider: **{task['provider']}**")
            
            if can_share_data(master_permission, task["share_data"]):
                st.info("✅ Sharing relevant data with provider.")
            else:
                st.warning("⚠️ Data sharing restricted.")

            if task["status"] == "Active":
                if st.button(f"Complete {task['task_name']}", key=f"complete_{i}"):
                    st.session_state.tasks[i]["status"] = "Done"
                    save_json(tasks_path, st.session_state.tasks)
                    st.rerun()

# --- RIGHT COLUMN: PROVIDER DISCOVERY ---
with right:
    st.subheader("Provider Discovery")
    category_list = ["Travel", "Food Delivery", "Home Service"]
    selected_cat = st.selectbox("Search Category", category_list)
    
    active_only = st.checkbox("Active Only", value=True)
    
    filtered = get_providers_by_category(st.session_state.providers, selected_cat, active_only)
    
    for p in filtered:
        with st.container(border=True):
            st.write(f"**{p['name']}**")
            st.caption(f"Trust Score: {p['trust']}%")
            if st.button(f"Select {p['name']}", key=f"select_{p['name']}"):
                st.success(f"Selected {p['name']} for future tasks!")
