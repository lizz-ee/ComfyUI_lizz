import json
from pathlib import Path

# Load the UI format workflow
workflow_path = Path(__file__).parent / "cliff_fall_ipadapter_multiseed.json"
with open(workflow_path, 'r', encoding='utf-8') as f:
    ui_workflow = json.load(f)

# Import the converter from the main script
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_cliff_fall import convert_workflow_to_api_format

# Convert
api_workflow = convert_workflow_to_api_format(ui_workflow)

# Save a sample
output_path = Path(__file__).parent / "test_api_format_sample.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(api_workflow, f, indent=2)

print(f"Converted workflow saved to: {output_path}")
print(f"\nSample of converted workflow (first 3 nodes):")
for i, (node_id, node_data) in enumerate(list(api_workflow.items())[:3]):
    print(f"\nNode {node_id}:")
    print(f"  class_type: {node_data['class_type']}")
    print(f"  inputs: {json.dumps(node_data['inputs'], indent=4)}")
