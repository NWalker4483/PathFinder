<?php
shell_exec("/usr/local/bin/gpio -g mode 17 out");
if($_GET['state']==="off"){ 
shell_exec("/usr/local/bin/gpio -g write 17 0"); 
}
else if($_GET['state']==="on")
{
shell_exec("/usr/local/bin/gpio -g write 17 1");
} 
else if($_GET['state']==="blink"){
for($x = 0;$x<=4;$x++)
{
shell_exec("/usr/local/bin/gpio -g write 17 1");
sleep(1);
shell_exec("/usr/local/bin/gpio -g write 17 0");
sleep(1);
}
}
?>