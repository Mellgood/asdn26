# Solutions for Lab 01

This lab introduces the CLI, so there are no custom Python scripts required to solve it. However, here are the expected answers to the questions in the tasks:

**Task 2:**
- **Tree topology `depth=2, fanout=2`**: 
  - Fanout 2 means each switch has 2 downlinks.
  - **Switches**: 1 root switch (s1), which connects to 2 child switches (s2, s3). **Total: 3 switches**.
  - **Hosts**: Each of the 2 leaf switches gets 2 hosts. **Total: 4 hosts (h1 to h4)**.

**Task 3:**
- Running `mn --link tc,bw=10,delay=10ms` adds a 10ms delay to each end of a link. Since ping measures Round Trip Time (RTT), the packet travels H1 -> S1 -> H2 (10+10 = 20ms) and back H2 -> S1 -> H1 (10+10 = 20ms).
- Actual `ping` results should show an RTT of approximately **~40ms**. The `iperf` bandwidth should cap close to **~10.0 Mbits/sec**.
