using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.IO;
using System.Net;
using System.Xml;
using System.Activities;
//using Microsoft.Activities.Messaging;

namespace GalileoAPITesting
{
    class Program
    {
        /// <summary>
        /// Creates a new account
        /// </summary>
        static void CreateNewAccount()
        {
            string sEndPoint = "https://sandbox-api.gpsrv.com/intserv/4.0/createAccount";
            string sAPICall = string.Format("{0}?apiLogin={1}&apiTransKey={2}&providerId={3}&transactionId={4}&prodId={5}", sEndPoint, "Dlm5Fn-9999", "QwQTu3mHXK", "488", "90917-random-string-34105", "501");

            string sResponse = HttpGet(sAPICall);
            XmlDocument doc = new XmlDocument();
            doc.LoadXml(sResponse);
            XmlNode xmlAPIResponse = doc.SelectSingleNode("response");

            HttpWebRequest req = WebRequest.Create(sAPICall) as HttpWebRequest;
            string sResponse = null;
            using (HttpWebResponse resp = req.GetResponse() as HttpWebResponse)
            {
                StreamReader reader = new StreamReader(resp.GetResponseStream());
                sResponse = reader.ReadToEnd();
            }
            XmlDocument doc = new XmlDocument();
            doc.LoadXml(sResponse);
            XmlNode xmlAPIResponse = doc.SelectSingleNode("response");

            Console.WriteLine(string.Format("{0} response code = {1}", sMethodName, xmlAPIResponse.FirstChild.InnerText));
        }

        static void Main(string[] args)
        {
            CreateNewAccount();
        }

    }
}
