import java.io.*;
import java.net.*;
import java.util.logging.Level; 
import java.util.logging.Logger; 
 
class client{ 
    static final String HOST="localhost"; 
    static final int PUERTO = 5000; 
     
    public client(){ 
        try { 
            System.out.println("INICIALIZANDO CLIENTE"); 
            Socket socketclient = new Socket(HOST, PUERTO); 
             
            InputStream mensajeDelServidor = socketclient.getInputStream(); 
            DataInputStream flujoSecuencial = new DataInputStream(mensajeDelServidor); 
            System.out.println(flujoSecuencial.readUTF()); 
             
            socketclient.close(); 
             
        } catch (IOException ex) { 
            Logger.getLogger(client.class.getName()).log(Level.SEVERE, null, ex); 
        } 
    } 
    
    public static void main(String[] arg){ 
        client nuevoCliente = new client(); 
    } 
