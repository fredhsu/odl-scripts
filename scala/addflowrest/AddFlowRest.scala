/**
 * Created with IntelliJ IDEA.
 * User: fhsu
 * Date: 5/27/13
 * Time: 2:21 PM
 * To change this template use File | Settings | File Templates.
 */

import dispatch._
import net.liftweb.json._
import net.liftweb.json.JsonDSL._

object AddFlowRest {

  implicit val formats = DefaultFormats
  val baseUrl = "http://localhost:8080/controller/nb/v2/"
  def fetchJson(urlString : String) = {
    println("Fetching " + urlString)
    val svc = url(urlString).as_!("admin", "admin")
    val result = Http(svc OK as.String)
    for (line <- result) println(line)
    parse(result()) //Have to make it a function call to avoid lazyniess
  }

  def pushJson(aUrl: String, jsonMap: String) {
    //Http(url(aUrl).POST << jsonMap
  }
               /*Http(url("http://exampleurl:8145/test") <<
  Map("tracker" -> "{'project':'campaign','event':'home','number':'100'}") >|)
  */


  def pushFlow() = {

    /* Example:
    val req = url("http://localhost:8983/update/json").POST.setBody("this")
    {"flowConfig":{"installInHw":"false","name":"test","node":{"@id":"00:00:00:00:00:00:00:01","@type":"OF"},
    "ingressPort":"1","priority":"500","etherType":"0x800","nwSrc":"10.0.0.1","nwDst":"10.0.0.3","actions":"OUTPUT=2"}}
    */
    // dlSrc = Data Link Src
    // Create a map that holds all the switches, and the flows to be pushed
    // Map(String, Map(String, String))
    val json =  (
      ("installInHw" -> "false") ~
        ("name"->"test2") ~
        ("node" -> ("@id"->"00:00:00:00:00:00:00:07") ~ ("@type" -> "OF")) ~
        ("ingressPort" -> "1") ~
        ("priority" -> "500") ~
        ("etherType" -> "0x800") ~
        ("nwSrc" -> "10.0.0.7") ~
        ("nwDst" -> "10.0.0.3") ~
        ("actions" -> "OUTPUT=2"))
    val jsonRequest = compact(render(json))
    println(jsonRequest)
    //val jsonRequest = """{"flowConfig":{"installInHw":"false","name":"test","node":{"@id":"00:00:00:00:00:00:00:01","@type":"OF"}, "ingressPort":"1","priority":"500","etherType":"0x800","nwSrc":"10.0.0.1","nwDst":"10.0.0.3","actions":"OUTPUT=2"}}"""
    //val myRequest = url(this.baseUrl + "flow/default/OF/00:00:00:00:00:00:00:07/test2").POST
    val myRequest = url(this.baseUrl + "flow/default/OF/00:00:00:00:00:00:00:07/test2/").POST
      .setBody(jsonRequest)
      .setHeader("Content-type", "application/json")
      .as_!("admin", "admin")
    println(myRequest)
    val result = Http(myRequest OK as.String)()
    println(result)
    //Maybe could do a map function over the items in the list
    /*
    val flow = """{"idleTimeout" : "180",
      "dlSrc" : "...",
      "protocol\" : "...",
      ""actions\" : [ \"...\", ... ],\n  \"ingressPort\" : \"...\",\n  \"priority\" : \"...\",\n  \"installInHw\" : \"...\",\n  \"tpSrc\" : \"...\",\n  \"node\" : {\n    \"id\" : \"...\",\n    \"type\" : \"...\"\n  },\n  \"name\" : \"...\",\n  \"nwDst\" : \"...\",\n  \"nwSrc\" : \"...\",\n  \"vlanId\" : \"...\",\n  \"dlDst\" : \"...\",\n  \"cookie\" : \"...\",\n  \"tosBits\" : \"...\",\n  \"hardTimeout\" : \"...\",\n  \"tpDst\" : \"...\"\n}"
    pushJson("http://localhost:8080/controller/nb/v2/topology/default", "key", "{}")
    */
  }
  def getFlows(containerName: String = "default") = {
    val getFlowUrl = this.baseUrl + "flow/" + containerName
    fetchJson(getFlowUrl)
  }
}

