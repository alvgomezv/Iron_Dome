<!DOCTYPE html>
<html>
<body>
  <h1>IronDome</h1>

  <p>
    IronDome is a Linux-based tool designed to detect anomalous activity and monitor different operating system parameters to identify potential ransomware attacks. By developing this program, you will gain insights into the weak points of a computer system with regard to malware infections.
  </p>

  <h2>Specifications</h2>

  <ul>
    <li>Platform: Linux</li>
    <li>Execution: Requires root access</li>
    <li>Execution Mode: Runs as a daemon or service in the background</li>
    <li>Monitoring Zone: A critical zone specified as a command-line argument</li>
    <li>File Extensions (optional): Specify file extensions to be observed as command-line arguments; if none provided, all files will be monitored</li>
    <li>Detection Features:
      <ul>
        <li>Disk Read Abuse: Detects abnormal disk read activities</li>
        <li>Intensive Cryptographic Activity: Identifies excessive cryptographic usage</li>
        <li>Changes in File Entropy: Detects alterations in file entropy</li>
      </ul>
    </li>
    <li>Memory Usage Limit: Program should not exceed 100 MB of memory usage</li>
    <li>Alert Reporting: All alerts will be logged in the <code>/var/log/irondome/irondome.log</code> file</li>
  </ul>

  <h2>Installation</h2>

  <ol>
    <li>Clone the IronDome repository to your local machine:</li>
  </ol>

  <pre><code>git clone https://github.com/alvgomezv/irondome.git</code></pre>

  <ol start="2">
    <li>Ensure that you have root access on your Linux machine to execute the program.</li>
    <li>Install the necessary dependencies, the dependencies for the bootcamp projects are in the globlar requirements.txt</li>
  </ol>

  <!--
  <h2>Usage</h2>

  <ol>
    <li>Open a terminal and navigate to the IronDome project directory:</li>
  </ol>

  <pre><code>cd irondome</code></pre>

  <ol start="2">
    <li>Launch IronDome as root:</li>
  </ol>

  <pre><code>sudo ./irondome /path/to/critical/zone [file extensions...]</code></pre>

  <p>
    Replace <code>/path/to/critical/zone</code> with the actual path of the critical zone you want to monitor. If you want to observe specific file extensions, provide them as additional command-line arguments. Otherwise, all files will be monitored.
  </p>

  <ol start="3">
    <li>IronDome will now run in the background as a daemon or service, continuously monitoring the specified critical zone and analyzing operating system parameters for potential ransomware activity.</li>
    <li>To view the alerts and notifications, check the <code>/var/log/irondome/irondome.log</code> file:</li>
  </ol>

  <pre><code>sudo cat /var/log/irondome/irondome.log</code></pre>

-->
