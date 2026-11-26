# Azure Cost Protection & Zero-Cost Safety Guide

**Target Budget**: Strictly ₹0.00 / $0.00  
**Directive**: Prevent accidental cloud infrastructure charges, credit card debits, or credit depletion.

---

## 1. Core Principles of Cloud Free Tiers

When evaluating Microsoft Azure for open-source hosting, developers often misunderstand billing mechanisms, leading to unexpected invoices.

### 1.1 Free Quota vs. Promotional Credits vs. Genuinely Free Hosting

| Category | Definition | Billing Danger |
| :--- | :--- | :--- |
| **Promotional Credits** | e.g. Azure Student (\$100) or Free Trial (\$200) granted for 30–365 days. | **HIGH DANGER**: Once credits expire or are depleted by a single forgotten resource, the subscription automatically transitions to Pay-As-You-Go and debits your credit card! |
| **12-Month Free Services** | Specific SKUs (e.g. B1s VM, 5 GB Blob storage) free for the first 12 months only. | **MODERATE DANGER**: If you accidentally select the wrong tier (e.g. B2s instead of B1s) or exceed egress bandwidth (15 GB/mo), you are charged immediately. |
| **Always Free Services** | Permanently free SKUs (e.g. Azure Static Web Apps Free tier, App Service F1). | **LOW TO MODERATE**: Supporting services (DNS, managed certs, log analytics, storage accounts) can quietly generate bills. |

> [!WARNING]
> **Promotional credits are NOT free hosting.** They are temporary allowances. Building on resources that require credits will inevitably result in a monthly bill once the credits lapse.

---

## 2. The Budget Alert Fallacy: Spending Cap vs. Budget Alert

Many developers create an **Azure Budget Alert** set to $1 or ₹100, believing that Azure will shut off resources when the limit is reached.

> [!CAUTION]
> **AN AZURE BUDGET ALERT DOES NOT STOP CHARGES!**  
> A budget alert only sends an automated email notifying you that spending occurred. **The resource continues running and accumulating charges** until manually deleted or until an explicit Azure Automation Runbook / webhook tears down the resource group.
>
> In contrast, an **Azure Spending Cap** (only available on specific Free Trial and MSDN subscriptions) actually blocks billing by suspending all resources. However, if a subscription is converted to Pay-As-You-Go, the spending cap is permanently removed and cannot be re-enabled!

---

## 3. Step-by-Step Manual Azure Verification Checklist

Before creating ANY resource in Azure, execute this manual audit in the [Azure Portal](https://portal.azure.com):

### Step 1: Verify Subscription Type
1. Search for **Subscriptions** in the top search bar.
2. Check the **Offer / Subscription Name**:
   - If it says **Pay-As-You-Go**, **STOP**. Do NOT deploy.
   - If it says **Azure for Students** or **Free Trial**, check the remaining credit balance and expiration date.
3. Check the **Spending Cap status**: Ensure it displays `Enabled`.

### Step 2: Audit Existing Resources & Costs
1. In the search bar, type **Cost Management + Billing**.
2. Navigate to **Cost Analysis** ➔ select **Current Month (Cumulative)**.
3. Confirm that current incurred charges are `₹0.00 / $0.00`.
4. Navigate to **All Resources** and verify no orphan disks, public IP addresses, container registries, or database servers exist.

### Step 3: Check Hidden Supporting Costs
Even when a compute resource is advertised as "free":
- **Public IP Addresses**: Standard static IPv4 addresses cost ~$3.60/month.
- **Storage Accounts**: Container images require an Azure Container Registry (Basic ACR costs ~$5/month).
- **Log Analytics Workspaces**: Diagnostic logs incur charges beyond 5 GB/month.
- **Bandwidth Egress**: Outbound data transfer beyond 15 GB/month is billed.

---

## 4. Azure Recommendation for AgriAI

Because Streamlit Community Cloud provides **100% genuine, permanent, public zero-cost hosting** without credit card registration or subscription expirations, **NO AZURE RESOURCES ARE REQUIRED OR PROVISIONED FOR THIS DEPLOYMENT**.

If an Azure presence is ever desired strictly for portfolio demonstration:
- **Only Azure Static Web Apps (Free SKU)** may be used to host a static HTML/JS landing page pointing to the Streamlit Community Cloud URL.
- **Never provision** Azure App Service, Azure Container Apps, or Azure Database for PostgreSQL for continuous zero-cost hosting.
