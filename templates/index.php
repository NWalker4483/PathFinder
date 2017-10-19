<?php
shell_exec("/usr/local/bin/gpio -g mode 17 out");
shell_exec("python ../pisces.py -p 4");
if($_GET['state']==="off"){ 
shell_exec("/usr/local/bin/gpio -g write 17 0"); 
shell_exec("python ../pisces.py -p 4 -s 700");
}
else if($_GET['state']==="on")
{
shell_exec("/usr/local/bin/gpio -g write 17 1");
shell_exec("python ../pisces.py -p 4 -s 1000");
} 
else if($_GET['state']==="blink"){
for($x = 0;$x<=4;$x++)
{
shell_exec("/usr/local/bin/gpio -g write 17 1");
shell_exec("python ../pisces.py -p 4 -s 1200");
sleep(1);
shell_exec("/usr/local/bin/gpio -g write 17 0");
shell_exec("python ../pisces.py -p 4 -s 700");
sleep(1);
}
}
?>