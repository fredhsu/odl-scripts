import dispatch._
import net.liftweb.json._

object Rest {

    implicit val formats = DefaultFormats
    def fetchJson(urlString : String) = {
        val svc = url(urlString).as_!("admin", "admin")
        val result = Http(svc OK as.String)
        for (line <- result) println(line)
        parse(result()) //Have to make it a function call to avoid lazyniess
        /*
        if (result().startsWith("\"")) {
            val clean = result().substring(1, result().length() - 1).replaceAll("\\", "")

            } else
        parse(result())
      */
    }

    def getIp() = {
        case class IpAddr(ip: String)
        val json = fetchJson("http://ip.jsontest.com/")
        json
        //json.extract[IpAddr]
    }

    def getTopo() = {
        val json = fetchJson("http://localhost:8080/controller/nb/v2/topology/default")
        json
    }

}
