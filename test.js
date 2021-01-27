function response(room, msg, sender, isGroupChat, replier, ImageDB, packageName) {
if (msg.charAt(0)=="$") {
    var data = org.jsoup.Jsoup
            .connect("http://andyye2.pythonanywhere.com/api/"+room+"@2@"+msg+"@2@"+sender+"@2@"+isGroupChat)
            .get()
            .select("body")
            .text ()+"";
    
    
    replier.reply(data); 
    }
}
