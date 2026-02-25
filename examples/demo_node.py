cat > examples/demo_node.py <<EOF
from src.node import NetworkNode

node = NetworkNode("DEMO_NODE")
node.start()
EOF
