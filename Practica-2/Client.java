import java.io.*;
import java.net.*; 
import java.util.Scanner; 
 
public class Client { 
    public static void main(String[] args) { 
        String host = "192.168.1.3"; 
        int port = 5000; 
 
        try ( 
            Socket socket = new Socket(host, port); 
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream())); 
            PrintWriter output = new PrintWriter(socket.getOutputStream(), true); 
            Scanner scanner = new Scanner(System.in) 
        ) { 
            System.out.println("Conectado al servidor."); 
 
            // Hilo para recibir mensajes del servidor 
            Thread receiveThread = new Thread(() -> { 
                try { 
                    String response; 
                    while ((response = input.readLine()) != null) { 
                        System.out.println("\nServidor: " + response); 
                        System.out.print("Cliente: "); // Mantener prompt 
                    } 
                } catch (IOException e) { 
                    System.out.println("Conexión cerrada."); 
                } 
            }); 
            receiveThread.start(); 
 
            // Hilo principal para enviar mensajes 
            String msg; 
            while (true) { 
                System.out.print("Cliente: "); 
                msg = scanner.nextLine(); 
                output.println(msg); 
                if ("salir".equalsIgnoreCase(msg)) { 
                    System.out.println("Cerrando conexión..."); 
                    break; 
                } 
            } 
 
        } catch (IOException e) { 
            System.out.println("No se pudo conectar al servidor. Asegúrate de que el servidor esté corriendo."); 
            e.printStackTrace(); 
        } 
    } 
}