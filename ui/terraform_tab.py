"""Terraform IaC agent interface tab."""
import streamlit as st
from agents.terraform_iac_agent import get_terraform_iac_agent
from utils.helpers import create_download_link

def render_terraform_tab():
    st.header("🛠️ Terraform IaC Agent")
    st.caption("Generate Terraform Infrastructure-as-Code configurations for AWS, Azure, and GCP data lakes")

    tf_agent = get_terraform_iac_agent()

    chat_sub, azure_sub, aws_gcp_sub = st.tabs(["💬 Chat", "🔷 Azure ADLS Gen2", "☁️ AWS & GCP"])

    with chat_sub:
        query = st.text_area("Ask about Terraform architecture configurations:",
                             placeholder="How can I create an Azure Databricks workspace with virtual network injection?",
                             key="tf_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="tf_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = tf_agent.process(query)
                    st.markdown(res)

    with azure_sub:
        st.subheader("Generate Azure ADLS Gen2 Config")
        rg_name = st.text_input("Resource Group Name", value="rg-data-prod", key="tf_az_rg")
        location = st.selectbox("Location", ["East US", "West US 2", "North Europe", "Southeast Asia"], key="tf_az_loc")
        storage_name = st.text_input("ADLS Storage Account Name", value="adlsstoreprod01", key="tf_az_store")
        if st.button("Generate Azure Resource", type="primary", key="tf_az_generate_btn"):
            code = tf_agent.generate_azure_infra(rg_name, location, storage_name)
            st.code(code, language="hcl")
            st.markdown(create_download_link(code, "azure_adls.tf"), unsafe_allow_html=True)

    with aws_gcp_sub:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("AWS S3 Config")
            bucket_name = st.text_input("AWS Bucket Name", value="my-prod-data-lake-bucket", key="tf_aws_bucket")
            if st.button("Generate AWS S3 Resource", type="primary", key="tf_aws_btn"):
                code = tf_agent.generate_aws_infra(bucket_name)
                st.code(code, language="hcl")
                st.markdown(create_download_link(code, "aws_s3.tf"), unsafe_allow_html=True)
        with col2:
            st.subheader("GCP GCS Config")
            project_id = st.text_input("GCP Project ID", value="my-gcp-project-id", key="tf_gcp_project")
            gcs_bucket = st.text_input("GCP Bucket Name", value="my-gcp-raw-data-bucket", key="tf_gcp_bucket")
            if st.button("Generate GCP Storage Resource", type="primary", key="tf_gcp_btn"):
                code = tf_agent.generate_gcp_infra(project_id, gcs_bucket)
                st.code(code, language="hcl")
                st.markdown(create_download_link(code, "gcp_gcs.tf"), unsafe_allow_html=True)
