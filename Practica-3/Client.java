import java.io.*; 
import java.net.*; 
import java.util.List; 
import java.util.Scanner; 
import com.google.gson.Gson; 
import com.google.gson.reflect.TypeToken; 
 
class Mensaje { 
    String usuario; 
    String mensaje; 
    String hora; 
} 
 
public class Client { 
    private static final String SERVER_URL = "http://127.0.0.1:5050"; 
    private static volatile boolean running = true; 
    private static String usuario; 
    private static int mensajesVistos = 0; 
    private static final Gson gson = new Gson(); 
 
    public static void main(String[] args) { 
        Scanner scanner = new Scanner(System.in); 
 
        System.out.print("Ingresa tu nombre de usuario: "); 
        usuario = scanner.nextLine().trim(); 
 
        System.out.println(" Conectado al chat. Escribe 'salir' para terminar."); 
 
        // Hilo para recibir mensajes continuamente 
        Thread recibirThread = new Thread(() -> { 
            while (running) { 
                recibirMensajes(); 
                try { 
                    Thread.sleep(1000); // actualiza cada segundo 
                } catch (InterruptedException e) { 
                    e.printStackTrace(); 
                } 
            } 
        }); 
        recibirThread.setDaemon(true); 
        recibirThread.start(); 
 
        // Hilo principal para enviar mensajes 
        while (true) { 
            String mensaje = scanner.nextLine().trim(); 
            if ("salir".equalsIgnoreCase(mensaje)) { 
                running = false; 
                break; 
            } 
            enviarMensaje(mensaje); 
        } 
 
        System.out.println("Cliente desconectado."); 
    } 
 
    private static void enviarMensaje(String mensaje) { 
        try { 
            URL url = new URL(SERVER_URL + "/enviar"); 
            HttpURLConnection conn = (HttpURLConnection) url.openConnection(); 
            conn.setRequestMethod("POST"); 
            conn.setRequestProperty("Content-Type", "application/json; utf-8"); 
            conn.setDoOutput(true); 
 
            String json = gson.toJson(new MensajeWrapper(usuario, mensaje)); 
 
            try (OutputStream os = conn.getOutputStream()) { 
                os.write(json.getBytes("utf-8")); 
            } 
 
            conn.getInputStream().close(); // ignorar respuesta 
 
        } catch (IOException e) { 
            System.out.println("Error al enviar mensaje: " + e.getMessage()); 
        } 
    } 
 
    private static void recibirMensajes() { 
        try { 
            URL url = new URL(SERVER_URL + "/recibir"); 
            HttpURLConnection conn = (HttpURLConnection) url.openConnection(); 
            conn.setRequestMethod("GET"); 
 
            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8")); 
            StringBuilder sb = new StringBuilder(); 
            String line; 
            while ((line = br.readLine()) != null) { 
                sb.append(line); 
            } 
            br.close(); 
 
            String json = sb.toString().trim(); 
            List<Mensaje> lista = gson.fromJson(json, new TypeToken<List<Mensaje>>(){}.getType()); 
 
            for (int i = mensajesVistos; i < lista.size(); i++) { 
                Mensaje m = lista.get(i); 
                System.out.println("[" + m.hora + "] " + m.usuario + ": " + m.mensaje); 
                mensajesVistos++; 
            } 
 
        } catch (IOException e) { 
            System.out.println("Error al recibir mensajes: " + e.getMessage()); 
        } 
    } 
 
    // Clase auxiliar para enviar mensajes 
    static class MensajeWrapper { 
        String usuario; 
        String mensaje; 
 
        MensajeWrapper(String usuario, String mensaje) { 
            this.usuario = usuario; 
            this.mensaje = mensaje; 
        } 
    } 
}