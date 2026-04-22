#!/bin/bash
# Direct path: h1 <-> s2 <-> s3 <-> h2

# Wait for mininet to be up
echo "Applying flows for direct path..."

# Note: Based on the Python script link order:
# s1-s2 (s2 port 1)
# s2-s3 (s2 port 2)
# h1-s2 (s2 port 3)
# --
# s1-s3 (s3 port 1)
# s2-s3 (s3 port 2)
# h2-s3 (s3 port 3)

# ----- S2 Flows -----
# 1. From h1 (port 3) forward to s3 (port 2)
ovs-ofctl add-flow s2 in_port=3,actions=output:2
# 2. Return path: From s3 (port 2) forward to h1 (port 3)
ovs-ofctl add-flow s2 in_port=2,actions=output:3

# ----- S3 Flows -----
# 1. From s2 (port 2) forward to h2 (port 3)
ovs-ofctl add-flow s3 in_port=2,actions=output:3
# 2. Return path: From h2 (port 3) forward to s2 (port 2)
ovs-ofctl add-flow s3 in_port=3,actions=output:2

echo "Flows applied. Test with 'h1 ping h2' in Mininet CLI."
