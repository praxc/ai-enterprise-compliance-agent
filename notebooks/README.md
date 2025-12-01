# Notebooks

## Available Notebooks

### `demo_compliance_agent.ipynb`
Complete demo notebook for the AI Enterprise Compliance Copilot.

**Contains:**
- Multi-agent system setup
- Policy and document loading
- Compliance check execution
- Dynamic result parsing
- Evaluation metrics

**Usage:**

**In Kaggle:**
1. Upload as new notebook
2. Add `GOOGLE_API_KEY` to Kaggle Secrets
3. Add `compliance-test-data` dataset (from `demo_data/`)
4. Run all cells

**Locally:**
1. Install dependencies: `pip install -r requirements.txt`
2. Set API key: `export GOOGLE_API_KEY="your-key"`
3. Run: `jupyter notebook demo_compliance_agent.ipynb`

## Files

- **demo_compliance_agent.ipynb**: Main demo (works in both Kaggle and locally)

## Note

The notebook is designed to work in both environments:
- In Kaggle: Reads test data from `/kaggle/input/compliance-test-data/`
- In Kaggle: Reads sample policy and scan doc form `/kaggle/input/sample-company-policy-data`
- Locally: Reads data from `../demo_data/`