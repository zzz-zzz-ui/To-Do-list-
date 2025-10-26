import streamlit as st

# 初始化任务列表
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

# 显示任务列表
def display_tasks():
    st.write("### 当前任务列表")
    if not st.session_state["tasks"]:
        st.write("任务列表为空！")
    else:
        for i, task in enumerate(st.session_state["tasks"]):
            status = "✅ 已完成" if task["completed"] else "❌ 未完成"
            st.write(f"{i + 1}. {task['name']} - {status}")

# 添加任务
def add_tasks(task_names):
    for name in task_names:
        st.session_state["tasks"].append({"name": name, "completed": False})

# 标记任务为完成
def mark_tasks_completed(task_indices):
    for index in task_indices:
        st.session_state["tasks"][index]["completed"] = True

# 删除任务
def delete_tasks(task_indices):
    for index in sorted(task_indices, reverse=True):
        del st.session_state["tasks"][index]

# 编辑任务
def edit_task(task_index, new_name):
    st.session_state["tasks"][task_index]["name"] = new_name

# Streamlit界面
st.title("任务管理器")
st.write("使用此应用程序管理您的任务清单。")

# 添加任务
st.write("### 添加任务")
task_input = st.text_area("请输入任务名称（每行一个任务）：")
if st.button("添加任务"):
    task_names = [name.strip() for name in task_input.split("\n") if name.strip()]
    if task_names:
        add_tasks(task_names)
        st.success(f"成功添加 {len(task_names)} 个任务！")
    else:
        st.warning("请输入至少一个任务名称！")

# 显示任务列表
display_tasks()

# 标记任务为完成
st.write("### 标记任务为完成")
if st.session_state["tasks"]:
    task_indices = st.multiselect(
        "选择要标记为完成的任务：",
        options=range(len(st.session_state["tasks"])),
        format_func=lambda x: st.session_state["tasks"][x]["name"],
    )
    if st.button("标记为完成"):
        if task_indices:
            mark_tasks_completed(task_indices)
            st.success(f"成功标记 {len(task_indices)} 个任务为完成！")
        else:
            st.warning("请选择至少一个任务！")
else:
    st.write("任务列表为空，无需标记。")

# 删除任务
st.write("### 删除任务")
if st.session_state["tasks"]:
    task_indices = st.multiselect(
        "选择要删除的任务：",
        options=range(len(st.session_state["tasks"])),
        format_func=lambda x: st.session_state["tasks"][x]["name"],
    )
    if st.button("删除任务"):
        if task_indices:
            delete_tasks(task_indices)
            st.success(f"成功删除 {len(task_indices)} 个任务！")
        else:
            st.warning("请选择至少一个任务！")
else:
    st.write("任务列表为空，无需删除。")

# 编辑任务
st.write("### 编辑任务")
if st.session_state["tasks"]:
    task_index = st.selectbox(
        "选择要编辑的任务：",
        options=range(len(st.session_state["tasks"])),
        format_func=lambda x: st.session_state["tasks"][x]["name"],
    )
    new_name = st.text_input("输入新的任务名称：", value=st.session_state["tasks"][task_index]["name"])
    if st.button("编辑任务"):
        if new_name.strip():
            edit_task(task_index, new_name.strip())
            st.success(f"任务已成功修改为 '{new_name}'！")
        else:
            st.warning("任务名称不能为空！")
else:
    st.write("任务列表为空，无需编辑。")