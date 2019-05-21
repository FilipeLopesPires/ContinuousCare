package com.example.pi_gps;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.location.Location;
import android.util.Log;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HurlStack;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.location.LocationResult;

import org.json.JSONObject;

import java.io.InputStream;
import java.security.KeyStore;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.HashMap;
import java.util.Map;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;

import static android.content.Context.MODE_PRIVATE;

public class GPSRestarter extends BroadcastReceiver {
    private Context context;

    public static String username=null;

    static final String ACTION_PROCESS_UPDATES =
            "com.google.android.gms.location.sample.backgroundlocationupdates.action" +
                    ".PROCESS_UPDATES";


    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent != null) {
            final String action = intent.getAction();
            if (ACTION_PROCESS_UPDATES.equals(action)) {
                LocationResult result = LocationResult.extractResult(intent);
                //Log.i(null, result.toString());
                if (result != null) {
                    this.context=context;
                    Location location = result.getLocations().get(0);

                    //Log.i(null, "aqui");

                    //Toast.makeText(context, location.getLatitude()+":"+location.getLongitude(), Toast.LENGTH_SHORT).show();

                    //,new HurlStack(null, getSocketFactory())
                    RequestQueue rq = (RequestQueue) Volley.newRequestQueue(context);

                    Map<String,Double> jsonMap = new HashMap();
                    jsonMap.put("latitude", location.getLatitude());
                    jsonMap.put("longitude", location.getLongitude());

                    SharedPreferences sp = context.getSharedPreferences("NameFile", MODE_PRIVATE);
                    String name = sp.getString("name", "");
                    Log.i(null, name);

                    JsonObjectRequest s = new JsonObjectRequest(Request.Method.POST,context.getResources().getString(R.string.gps_endpoint,name),new JSONObject(jsonMap),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject s) {
                                    Log.i(null,s.toString());

                                }
                            },

                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError volleyError) {
                                    Log.e("RESULTfailder",volleyError.toString()); }
                            } );

                    rq.add(s);


                }
            }
        }
    }


    private SSLSocketFactory getSocketFactory() {
        /*
        Request and timer
        RequestQueue rq = Volley.newRequestQueue(this, new HurlStack(null, getSocketFactory()));

        Map<String,String> jsonMap = new HashMap();
        jsonMap.put("chave", "valor");

        JsonObjectRequest s = new JsonObjectRequest(Request.Method.POST,  "https://192.168.43.136:5000/teste",new JSONObject(jsonMap),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject s) {
                        Toast.makeText(getApplicationContext(),s.toString(), Toast.LENGTH_LONG).show();

                    }
                },

                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError volleyError) {
                        Log.e("RESULTfailder",volleyError.getMessage()); }
                } );

        rq.add(s);


        if(count==0) {
            T.scheduleAtFixedRate(new TimerTask() {
                @Override
                public void run() {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //DoStuff
                        }
                    });
                }
            }, 1000, 5000);

        }

        count++;
        if(count>1){
            T.cancel();
        }
        */

        CertificateFactory cf = null;
        try {
            cf = CertificateFactory.getInstance("X.509");
            InputStream caInput = this.context.getResources().openRawResource(R.raw.my_cert);
            Certificate ca;
            try {
                ca = cf.generateCertificate(caInput);
                Log.e("CERT", "ca=" + ((X509Certificate) ca).getSubjectDN());
            } finally {
                caInput.close();
            }


            String keyStoreType = KeyStore.getDefaultType();
            KeyStore keyStore = KeyStore.getInstance(keyStoreType);
            keyStore.load(null, null);
            keyStore.setCertificateEntry("ca", ca);


            String tmfAlgorithm = TrustManagerFactory.getDefaultAlgorithm();
            TrustManagerFactory tmf = TrustManagerFactory.getInstance(tmfAlgorithm);
            tmf.init(keyStore);


            HostnameVerifier hostnameVerifier = new HostnameVerifier() {
                @Override
                public boolean verify(String hostname, SSLSession session) {

                    Log.e("CipherUsed", session.getCipherSuite());
                    return hostname.compareTo("192.168.43.136")==0; //The Hostname of your server

                }
            };


            HttpsURLConnection.setDefaultHostnameVerifier(hostnameVerifier);
            SSLContext context = null;
            context = SSLContext.getInstance("TLS");

            context.init(null, tmf.getTrustManagers(), null);
            HttpsURLConnection.setDefaultSSLSocketFactory(context.getSocketFactory());

            SSLSocketFactory sf = context.getSocketFactory();


            return sf;

        } catch (Exception e) {
            e.printStackTrace();
        }

        return  null;
    }
}