
import streamlit as st
from workflow.graph import build_graph


# Initialize LangGraph only once
@st.cache_resource
def get_graph():
    return build_graph()


graph = get_graph()


# Convert Gemini response into readable text
def normalize_output(value):

    if isinstance(value, str):
        return value

    if isinstance(value, list):
        parts = []

        for item in value:
            if isinstance(item, dict):
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))

        return "\n".join(parts)

    return str(value)


# Page configuration
st.set_page_config(
    page_title="NyayaAI - Consumer Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)


# Application heading
st.title("⚖️ NyayaAI")
st.subheader("AI-powered Indian Consumer Dispute Assistant")

st.info(
    "NyayaAI provides general legal information "
    "and preliminary complaint drafts. It is not "
    "a substitute for a qualified lawyer."
)


# User input
st.markdown("### Describe Your Consumer Dispute")

user_query = st.text_area(
    "Explain what happened:",
    height=180,
    placeholder=(
        "Example: I purchased a mobile phone for "
        "Rs. 20000 from Amazon. It arrived with a "
        "damaged screen, but the seller refused "
        "to provide a refund."
    )
)


# Analyze button
if st.button("Analyze My Case", type="primary"):

    if not user_query.strip():
        st.warning("Please describe your consumer dispute.")

    else:
        with st.spinner(
            "NyayaAI is analyzing your case..."
        ):

            try:
                initial_state = {
                    "user_query": user_query
                }

                result = graph.invoke(initial_state)

                st.session_state["result"] = result

                st.success("Case analysis completed!")

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)


# Display results
if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.markdown("## Analysis Results")

    # Issue category
    st.markdown("### Identified Issue")

    st.write(
        result.get("issue_category", "Not identified")
    )

    # Legal advice
    st.markdown("### Legal Advice")

    legal_answer = normalize_output(
        result.get("legal_answer", "")
    )

    st.markdown(legal_answer)

    st.divider()

    # Generated complaint
    st.markdown("## Preliminary Consumer Complaint")

    complaint = normalize_output(
        result.get("generated_document", "")
    )

    st.markdown(complaint)

    # Download complaint
    st.download_button(
        label="Download Complaint",
        data=complaint,
        file_name="NyayaAI_Consumer_Complaint.txt",
        mime="text/plain"
    )
