import streamlit as st

providers = [
    {
        "name": "RailYatri Mock",
        "category": "Travel",
        "collab_ready": True,
        "active": True,
        "available": True,
        "trust": 85
    },
    {
        "name": "Zomato Mock",
        "category": "Food Delivery",
        "collab_ready": True,
        "active": True,
        "available": True,
        "trust": 88
    },
    {
        "name": "Swiggy Mock",
        "category": "Food Delivery",
        "collab_ready": False,
        "active": True,
        "available": True,
        "trust": 80
    },
    {
        "name": "RepairHub Mock",
        "category": "Home Service",
        "collab_ready": True,
        "active": True,
        "available": True,
        "trust": 75
    }
]

initial_customer = {
    "name": "Aditya Dubey",
    "phone": "9876543210",
    "email": "aditya.dby211@email.com",
    "address": "Bhopal, india",
    "medical_conditions": ["Liver"],
    "health_id": "UHID12345",
    "food_choice": "Veg",
    "spice_level": "Medium",
    "payment_mode": "UPI",
    "other_info": "Window seat preference"
}

initial_tasks = [
    {
        "task_name": "Book Train",
        "category": "Travel",
        "provider": "RailYatri Mock",
        "dependency": "Independent",
        "status": "Done",
        "share_data": True
    },
    {
        "task_name": "Order Food",
        "category": "Food Delivery",
        "provider": "Zomato Mock",
        "dependency": "After previous task",
        "status": "Pending",
        "share_data": True
    }
]

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

def update_task_flow(tasks):
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

def can_share_data(master_permission, task_permission):
    return master_permission and task_permission

st.set_page_config(page_title="Life Canvas", layout="wide")

categories = ["Travel", "Food Delivery", "Home Service", "Healthcare"]

if "customer" not in st.session_state:
    st.session_state.customer = initial_customer.copy()

if "tasks" not in st.session_state:
    st.session_state.tasks = [task.copy() for task in initial_tasks]

if "provider_filter_active" not in st.session_state:
    st.session_state.provider_filter_active = False

if "provider_filter_collab" not in st.session_state:
    st.session_state.provider_filter_collab = False

provider_dict = {p["name"]: p for p in providers}

st.title("Life Canvas")
st.caption("Your Data. Your Money. Your Terms.")

left, center, right = st.columns([1.1, 1.4, 1.1])

with left:
    st.subheader("Customer Registration Vault")

    with st.form("customer_form"):
        name = st.text_input("Full Name", st.session_state.customer["name"])
        phone = st.text_input("Phone", st.session_state.customer["phone"])
        email = st.text_input("Email", st.session_state.customer["email"])
        address = st.text_input("Address", st.session_state.customer["address"])
        health_id = st.text_input("Universal Health ID", st.session_state.customer["health_id"])
        food_choice = st.selectbox(
            "Food Choice",
            ["Veg", "Non-Veg", "Vegan", "Jain"],
            index=["Veg", "Non-Veg", "Vegan", "Jain"].index(st.session_state.customer.get("food_choice", "Veg"))
        )
        spice = st.selectbox(
            "Spice Level",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(st.session_state.customer.get("spice_level", "Medium"))
        )
        payment = st.selectbox(
            "Payment Mode",
            ["UPI", "Card", "Cash"],
            index=["UPI", "Card", "Cash"].index(st.session_state.customer.get("payment_mode", "UPI"))
        )
        other = st.text_input("Other Shared Info", st.session_state.customer.get("other_info", ""))
        submitted = st.form_submit_button("Save Profile")

        if submitted:
            st.session_state.customer.update({
                "name": name,
                "phone": phone,
                "email": email,
                "address": address,
                "health_id": health_id,
                "food_choice": food_choice,
                "spice_level": spice,
                "payment_mode": payment,
                "other_info": other
            })
            st.success("Profile saved")

    master_permission = st.toggle("Allow sharing selected profile fields", value=True)

with center:
    st.subheader("Life Canvas")

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("Travel + Food", use_container_width=True):
            st.session_state.tasks = [
                {
                    "task_name": "Book Train",
                    "category": "Travel",
                    "provider": "RailYatri Mock",
                    "dependency": "Independent",
                    "status": "Done",
                    "share_data": True
                },
                {
                    "task_name": "Order Food",
                    "category": "Food Delivery",
                    "provider": "Zomato Mock",
                    "dependency": "After previous task",
                    "status": "Pending",
                    "share_data": True
                }
            ]
            st.rerun()

    with b2:
        if st.button("Event Planning", use_container_width=True):
            st.session_state.tasks = [
                {
                    "task_name": "Book Venue",
                    "category": "Home Service",
                    "provider": "RepairHub Mock",
                    "dependency": "Independent",
                    "status": "Done",
                    "share_data": True
                },
                {
                    "task_name": "Order Catering",
                    "category": "Food Delivery",
                    "provider": "Zomato Mock",
                    "dependency": "After previous task",
                    "status": "Pending",
                    "share_data": True
                }
            ]
            st.rerun()

    with b3:
        if st.button("Home Repair", use_container_width=True):
            st.session_state.tasks = [
                {
                    "task_name": "Raise Repair Request",
                    "category": "Home Service",
                    "provider": "RepairHub Mock",
                    "dependency": "Independent",
                    "status": "Active",
                    "share_data": True
                }
            ]
            st.rerun()

    st.text_input("What do you want to do today?", "Travel + food coordination")

    for i, task in enumerate(st.session_state.tasks):
        with st.container(border=True):
            c1, c2 = st.columns([2, 1])

            with c1:
                task["task_name"] = st.text_input(f"Task Name {i}", task["task_name"], key=f"name_{i}")

                task["category"] = st.selectbox(
                    f"Category {i}",
                    categories,
                    index=categories.index(task["category"]),
                    key=f"cat_{i}"
                )

                provider_options = get_providers_by_category(
                    providers,
                    task["category"],
                    active_only=st.session_state.provider_filter_active,
                    collab_only=st.session_state.provider_filter_collab
                )
                provider_names = [p["name"] for p in provider_options]

                if not provider_names:
                    st.warning(f"No providers available for {task['category']}.")
                    task["provider"] = ""
                    st.selectbox(f"Provider {i}", ["No provider found"], disabled=True, key=f"provider_{i}")
                else:
                    if task["provider"] not in provider_names:
                        task["provider"] = provider_names[0]

                    task["provider"] = st.selectbox(
                        f"Provider {i}",
                        provider_names,
                        index=provider_names.index(task["provider"]),
                        key=f"provider_{i}"
                    )

                task["dependency"] = st.selectbox(
                    f"Dependency {i}",
                    ["Independent", "After previous task", "Parallel"],
                    index=["Independent", "After previous task", "Parallel"].index(task["dependency"]),
                    key=f"dep_{i}"
                )

                task["share_data"] = st.checkbox(
                    "Allow sharing previous task context",
                    value=task["share_data"],
                    key=f"share_{i}"
                )

            with c2:
                task["status"] = st.selectbox(
                    f"Status {i}",
                    ["Pending", "Active", "Done", "Delayed", "Blocked"],
                    index=["Pending", "Active", "Done", "Delayed", "Blocked"].index(task["status"]),
                    key=f"status_{i}"
                )

                selected_provider = provider_dict.get(task["provider"])
                if selected_provider:
                    if selected_provider["collab_ready"]:
                        st.badge("Collab Ready", icon="🤝")
                    if selected_provider["active"]:
                        st.badge("Active Communicator", icon="🟢")
                    st.metric("Trust Score", selected_provider["trust"])

        st.markdown("➕")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add New Task"):
            st.session_state.tasks.append({
                "task_name": f"Task {len(st.session_state.tasks) + 1}",
                "category": "Home Service",
                "provider": "RepairHub Mock",
                "dependency": "Independent",
                "status": "Pending",
                "share_data": False
            })
            st.rerun()

    with col2:
        if st.button("Run Orchestration"):
            st.session_state.tasks = update_task_flow(st.session_state.tasks)
            st.success("Workflow updated")

    for i, task in enumerate(st.session_state.tasks):
        if i > 0 and task["dependency"] == "After previous task":
            prev_task = st.session_state.tasks[i - 1]

            if prev_task["status"] == "Delayed":
                backup = suggest_backup(providers, task["category"], task["provider"])
                st.warning(f"Task {i+1} blocked due to delay. Suggested backup: {backup}")

            if can_share_data(master_permission, task["share_data"]):
                st.info(f"Task {i+1} can access previous task context")

    st.markdown("---")
    st.subheader("Final Collaboration Approval")

    customer_collab_approval = st.toggle("Customer approves provider collaboration", value=True)

    if customer_collab_approval:
        st.success("Collaboration approved by customer")
    else:
        st.warning("Providers must work independently")

    st.markdown("---")
    st.markdown("### Cross-Platform Trust Summary")

    completed_tasks = sum(1 for t in st.session_state.tasks if t["status"] == "Done")
    delayed_tasks = sum(1 for t in st.session_state.tasks if t["status"] == "Delayed")
    trust_score = max(50, 100 - delayed_tasks * 10 + completed_tasks * 5)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Completed Tasks", completed_tasks)
    with m2:
        st.metric("Delayed Tasks", delayed_tasks)
    with m3:
        st.metric("Workflow Trust Score", f"{trust_score}/100")

with right:
    st.subheader("Provider Discovery")

    st.session_state.provider_filter_active = st.checkbox(
        "Active communicators only",
        value=st.session_state.provider_filter_active
    )

    st.session_state.provider_filter_collab = st.checkbox(
        "Collab-ready only",
        value=st.session_state.provider_filter_collab
    )

    selected_category = st.selectbox("Filter by category", ["All"] + categories)

    shown_providers = providers

    if selected_category != "All":
        shown_providers = [p for p in shown_providers if p["category"] == selected_category]

    if st.session_state.provider_filter_active:
        shown_providers = [p for p in shown_providers if p["active"]]

    if st.session_state.provider_filter_collab:
        shown_providers = [p for p in shown_providers if p["collab_ready"]]

    for p in shown_providers:
        with st.container(border=True):
            st.write(f"**{p['name']}**")
            st.write(p["category"])
            if p["active"]:
                st.badge("Active Communicator", icon="🟢")
            if p["collab_ready"]:
                st.badge("Collab Ready", icon="🤝")
            st.write(f"Trust Score: {p['trust']}")
            st.write("Available" if p["available"] else "Unavailable")

    st.info("Mock data now; real APIs can replace provider and task sources later.")