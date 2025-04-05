#!/bin/bash

# Updated run_bank.sh
# This script opens multiple terminal windows, runs a series of client commands,
# and prints messages to show which command is executing.
# An optional dynamic testing loop is included at the end for stress-testing.

echo "Starting server in a new terminal..."
gnome-terminal -- bash -c "echo 'Starting server.py...'; python3 server.py; exec bash"
sleep 3  # Wait 3 seconds to allow the server to start

# ---------------- Client Terminal 1 ----------------
gnome-terminal -- bash -c "
echo 'Client Terminal 1: Running test transactions...';

echo 'Command: Audit show_bank';
python3 client.py Audit show_bank;
sleep 1;

echo 'Command: Bob deposits 3500 into account 1003';
python3 client.py Bob deposit 1003 3500;
sleep 1;

echo 'Command: Tim creates account 1078 with initial deposit 500';
python3 client.py Tim create_account 1078 500;
sleep 1;

echo 'Command: Alice withdraws 2000 from account 1001';
python3 client.py Alice withdraw 1001 2000;
sleep 1;

echo 'Command: Alice pays loan check on account 1002 with 100';
python3 client.py Alice pay_loan_check 1002 100;
sleep 1;

echo 'Command: William transfers 200 to account 1013';
python3 client.py William transfer_to 1013 200;
sleep 1;

echo 'Command: Ivan pays loan check on account 1016 with 300';
python3 client.py Ivan pay_loan_check 1016 300;
sleep 1;

echo 'Command: Tim deposits 5000 into account 1078';
python3 client.py Tim deposit 1078 5000;
sleep 1;

echo 'Command: Tim withdraws 2000 from account 1078';
python3 client.py Tim withdraw 1078 2000;
sleep 1;

echo 'Command: Frank withdraws 200 from account 1009';
python3 client.py Frank withdraw 1009 200;
exec bash"

# ---------------- Client Terminal 2 ----------------
gnome-terminal -- bash -c "
echo 'Client Terminal 2: Running test transactions...';

echo 'Command: Audit show_bank';
python3 client.py Audit show_bank;
sleep 1;

echo 'Command: Ivan deposits 2100 into account 1003';
python3 client.py Ivan deposit 1003 2100;
sleep 1;

echo 'Command: Zion creates account 1099 with initial deposit 2000';
python3 client.py Zion create_account 1099 2000;
sleep 1;

echo 'Command: Tim withdraws 100 from account 1078';
python3 client.py Tim withdraw 1078 100;
sleep 1;

echo 'Command: Alice shows history for account 1001';
python3 client.py Alice show_history 1001;
sleep 1;

echo 'Command: Heidi pays loan check on account 1014 with 100';
python3 client.py Heidi pay_loan_check 1014 100;
sleep 1;

echo 'Command: Zion transfers 500 to account 1078';
python3 client.py Zion transfer_to 1078 500;
sleep 1;

echo 'Command: Alice pays loan transfer on account 1002 with 100';
python3 client.py Alice pay_loan_transfer_to 1002 100;
sleep 1;

echo 'Command: Tim withdraws 50 from account 1078';
python3 client.py Tim withdraw 1078 50;
sleep 1;

echo 'Command: Dora creates account 1234';
python3 client.py Dora create_account 1234;
exec bash"

# ---------------- Client Terminal 3 ----------------
gnome-terminal -- bash -c "
echo 'Client Terminal 3: Running test transactions...';

echo 'Command: Audit show_bank';
python3 client.py Audit show_bank;
sleep 1;

echo 'Command: Kevin deposits 700 into account 1003';
python3 client.py Kevin deposit 1003 700;
sleep 1;

echo 'Command: Henry deposits 300 into account 1054';
python3 client.py Henry deposit 1054 300;
sleep 1;

echo 'Command: James withdraws 300 from account 1021';
python3 client.py James withdraw 1021 300;
sleep 1;

echo 'Command: Alice deposits 5000 into account 1001';
python3 client.py Alice deposit 1001 5000;
sleep 1;

echo 'Command: William transfers 100 to account 1078';
python3 client.py William transfer_to 1078 100;
sleep 1;

echo 'Command: Paul transfers 200 to account 1035';
python3 client.py Paul transfer_to 1035 200;
sleep 1;

echo 'Command: James shows history for account 1021';
python3 client.py James show_history 1021;
sleep 1;

echo 'Command: Robert pays loan transfer on account 1026 with 100';
python3 client.py Robert pay_loan_transfer_to 1026 100;
sleep 1;

echo 'Command: Tim withdraws 100 from account 1078';
python3 client.py Tim withdraw 1078 100;
exec bash"

# ---------------- Client Terminal 4 ----------------
gnome-terminal -- bash -c "
echo 'Client Terminal 4: Running test transactions...';

echo 'Command: Audit show_bank';
python3 client.py Audit show_bank;
sleep 1;

echo 'Command: Bob withdraws 900 from account 1003';
python3 client.py Bob withdraw 1003 900;
sleep 1;

echo 'Command: David withdraws 600 from account 1029';
python3 client.py David withdraw 1029 600;
sleep 1;

echo 'Command: David shows history for account 1029';
python3 client.py David show_history 1029;
sleep 1;

echo 'Command: Mark deposits 2200 into account 1034';
python3 client.py Mark deposit 1034 2200;
sleep 1;

echo 'Command: Kate transfers 100 to account 1015';
python3 client.py Kate transfer_to 1015 100;
sleep 1;

echo 'Command: Charlie withdraws 2800 from account 1005';
python3 client.py Charlie withdraw 1005 2800;
sleep 1;

echo 'Command: Dave transfers 100 to account 1009';
python3 client.py Dave transfer_to 1009 100;
sleep 1;

echo 'Command: John withdraws 600 from account 1017';
python3 client.py John withdraw 1017 600;
sleep 1;

echo 'Command: Justin deposits 3100 into account 1047';
python3 client.py Justin deposit 1047 3100;
exec bash"

# ---------------- Optional: Dynamic Testing Loop ----------------
# Uncomment the following block to continuously run random transactions for stress-testing.

: '
gnome-terminal -- bash -c "
echo 'Dynamic Testing: Random transactions loop started...';
while true; do
    cmd=\$(shuf -n1 -e \
        \"python3 client.py Alice deposit 1001 100\" \
        \"python3 client.py Bob withdraw 1003 50\" \
        \"python3 client.py Charlie transfer_to 1015 25\" \
        \"python3 client.py David show_history 1029\" );
    echo \"Executing random command: \$cmd\";
    eval \$cmd;
    sleep 1;
done;
exec bash"
'
