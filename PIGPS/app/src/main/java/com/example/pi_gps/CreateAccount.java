package com.example.pi_gps;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HurlStack;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.io.InputStream;
import java.security.KeyStore;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;

public class CreateAccount extends AppCompatActivity implements View.OnClickListener {

    private TextView username, password, fullname, phpn, email, weight, height, diseases;
    private DatePicker birthdate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_account);

        Button create=(Button) findViewById(R.id.create);
        username=(TextView) findViewById(R.id.username);
        password=(TextView) findViewById(R.id.password);
        fullname=(TextView) findViewById(R.id.fullname);
        phpn=(TextView) findViewById(R.id.phpn);
        email=(TextView) findViewById(R.id.email);
        birthdate=(DatePicker) findViewById(R.id.birthdate);
        weight=(TextView) findViewById(R.id.weight);
        height=(TextView) findViewById(R.id.height);
        diseases=(TextView) findViewById(R.id.diseases);

        create.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.create:

                RequestQueue rq = Volley.newRequestQueue(this, new HurlStack(null, getSocketFactory()));

                Map<String, String> jsonMap = new HashMap();
                jsonMap.put("username", (String) username.getText().toString());
                jsonMap.put("password",(String) password.getText().toString());
                jsonMap.put("name",(String) fullname.getText().toString());
                jsonMap.put("phpn",(String) phpn.getText().toString());
                jsonMap.put("email",(String) email.getText().toString());
                int day = birthdate.getDayOfMonth();
                int month = birthdate.getMonth();
                int year =  birthdate.getYear();
                jsonMap.put("birth_date",(String) (day+"-"+month+"-"+year));
                jsonMap.put("weight",(String) weight.getText().toString());
                jsonMap.put("height",(String) height.getText().toString());
                jsonMap.put("diseases",(String) diseases.getText().toString());

                JsonObjectRequest s = new JsonObjectRequest(Request.Method.POST, getResources().getString(R.string.endpoint, "signup"), new JSONObject(jsonMap),
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject s) {
                                Toast.makeText(getApplicationContext(), s.toString(), Toast.LENGTH_LONG).show();
                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError volleyError) {
                                new Response.ErrorListener() {
                                    @Override
                                    public void onErrorResponse(VolleyError volleyError) {
                                        Log.e("FAIL", volleyError.toString());
                                    }
                                };
                            }
                        });

                rq.add(s);

                break;
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

    */

        CertificateFactory cf = null;
        try {
            cf = CertificateFactory.getInstance("X.509");
            InputStream caInput = getResources().openRawResource(R.raw.my_cert);
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
