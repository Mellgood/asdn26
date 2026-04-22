# Solutions for Lab 03

There is no Python script required for this lab, but here is the expected execution sequence:

1. **In Terminal 1:**
   ```bash
   root@host:/lab# mn --topo single,2 --controller none
   *** Creating network
   *** Adding controller
   *** Adding hosts:
   h1 h2 
   ...
   mininet> h1 ping -c 3 h2  
   # Output will be: Destination Host Unreachable or 100% packet loss
   ```

2. **In Terminal 2 (while Terminal 1 is open):**
   ```bash
   root@host:/lab# ovs-vsctl show
   ... shows Bridge "s1" with Port "s1-eth1" and Port "s1-eth2"
   
   root@host:/lab# ovs-ofctl dump-flows s1  
   # Output: empty
   
   # Inject the rules (creating a simple L1 patch cable between port 1 and 2)
   root@host:/lab# ovs-ofctl add-flow s1 in_port=1,actions=output:2
   root@host:/lab# ovs-ofctl add-flow s1 in_port=2,actions=output:1
   
   root@host:/lab# ovs-ofctl dump-flows s1  
   # Output:
   # cookie=0x0, duration=2.1s, table=0, n_packets=0, n_bytes=0, in_port=1 actions=output:2
   # cookie=0x0, duration=1.2s, table=0, n_packets=0, n_bytes=0, in_port=2 actions=output:1
   ```

3. **Back in Terminal 1:**
   ```bash
   mininet> h1 ping -c 3 h2  
   # Succeeds!
   # 3 packets transmitted, 3 received, 0% packet loss
   ```
