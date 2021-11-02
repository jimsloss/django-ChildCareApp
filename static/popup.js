function hello()
{
    var thetime = new Date();
    var newtime = thetime.getDate() +'/'+(thetime.getMonth()+1)+'/'+thetime.getFullYear();
    newtime = "Today is: " + newtime +  "\n \n Need to select new date here \n\n Use Modal instead?";
    alert(newtime);
}   


