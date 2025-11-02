import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge

# 初始化任务列表
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

# 显示任务列表
def display_tasks(search_query=None):
    st.write("### 当前任务列表")
    if not st.session_state["tasks"]:
        st.write("任务列表为空！")
    else:
        filtered_tasks = st.session_state["tasks"]
        if search_query:
            filtered_tasks = [task for task in st.session_state["tasks"] if search_query.lower() in task["name"].lower()]
        
        if not filtered_tasks:
            st.write("未找到匹配的任务！")
        else:
            for i, task in enumerate(filtered_tasks):
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
badge("github", "https://github.com/streamlit/streamlit-extras")

# 添加垂直间距
add_vertical_space(2)

# 顶部导航栏
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.write("### 添加任务")
    task_input = st.text_area("请输入任务名称（每行一个任务）：", key="add_task_input")
    if st.button("➕ 添加任务", key="add_task_button"):
        task_names = [name.strip() for name in task_input.split("\n") if name.strip()]
        if task_names:
            add_tasks(task_names)
            st.success(f"成功添加 {len(task_names)} 个任务！")
        else:
            st.warning("请输入至少一个任务名称！")

with col2:
    st.write("### 标记任务为完成")
    if st.session_state["tasks"]:
        task_indices = st.multiselect(
            "选择要标记为完成的任务：",
            options=range(len(st.session_state["tasks"])),
            format_func=lambda x: st.session_state["tasks"][x]["name"],
            key="mark_task_multiselect"
        )
        if st.button("✅ 标记完成", key="mark_task_button"):
            if task_indices:
                mark_tasks_completed(task_indices)
                st.success(f"成功标记 {len(task_indices)} 个任务为完成！")
            else:
                st.warning("请选择至少一个任务！")
    else:
        st.write("任务列表为空，无需标记。")

with col3:
    st.write("### 删除任务")
    if st.session_state["tasks"]:
        task_indices = st.multiselect(
            "选择要删除的任务：",
            options=range(len(st.session_state["tasks"])),
            format_func=lambda x: st.session_state["tasks"][x]["name"],
            key="delete_task_multiselect"
        )
        if st.button("🗑️ 删除任务", key="delete_task_button"):
            if task_indices:
                delete_tasks(task_indices)
                st.success(f"成功删除 {len(task_indices)} 个任务！")
            else:
                st.warning("请选择至少一个任务！")
    else:
        st.write("任务列表为空，无需删除。")

with col4:
    st.write("### 编辑任务")
    if st.session_state["tasks"]:
        task_index = st.selectbox(
            "选择要编辑的任务：",
            options=range(len(st.session_state["tasks"])),
            format_func=lambda x: st.session_state["tasks"][x]["name"],
            key="edit_task_selectbox"
        )
        new_name = st.text_input("输入新的任务名称：", value=st.session_state["tasks"][task_index]["name"], key="edit_task_input")
        if st.button("✏️ 编辑任务", key="edit_task_button"):
            if new_name.strip():
                edit_task(task_index, new_name.strip())
                st.success(f"任务已成功修改为 '{new_name}'！")
            else:
                st.warning("任务名称不能为空！")
    else:
        st.write("任务列表为空，无需编辑。")

with col5:
    st.write("### 搜索任务")
    search_query = st.text_input("输入搜索关键词：", key="search_task_input")
    if st.button("🔍 搜索任务", key="search_task_button"):
        st.write("---")
        display_tasks(search_query)

# 显示任务列表
st.write("---")
display_tasks()