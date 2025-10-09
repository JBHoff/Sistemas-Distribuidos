//package Practica_1;

import java.io.*; 
import java.net.*; 
 
class server{ 
    static final int PUERTO=5000; 
    public server(){ 
        try { 
            System.out.println("inicializando Servidor"); 
            ServerSocket socketserver = new ServerSocket(PUERTO); 
            System.out.println("Escucho el puerto" + PUERTO); 
            System.out.println("esperando conexiones de clientes "); 
             
            for (int numeroCliente = 0; numeroCliente <3; numeroCliente++){ 
                Socket socketclient=socketserver.accept(); 
                System.out.println("sirvo al cliente" +numeroCliente + "en el puerto de comunicación" +socketclient.getPort()); 
                OutputStream mensajeParaCliente= socketclient.getOutputStream(); 
                DataOutputStream flujoSecuencial=new DataOutputStream(mensajeParaCliente); 
                flujoSecuencial.writeUTF("bienvenido cliente" + numeroCliente+".\nEl puerto de escucha es el numero" +socketclient.getLocalPort()+"y el puerto de comunicacion bidireccional es "+socketclient.getPort()); 
                socketclient.close(); 
            } 
             
            System.out.println("demasiados clientes "); 
            System.out.println("solamente aceptamos 3 clientes"); 
        } catch (Exception e) { 
             
        System.out.println( e.getMessage()); 
    } 
} 
 
public static void main(String[] arg) { 
    server miServidor=new server(); 
    } 
}