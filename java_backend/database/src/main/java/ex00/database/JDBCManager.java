package ex00.database;

import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class JDBCManager {
    private static JDBCManager instance;
    private String dbUrl;
    private String dbUsername;
    private String dbPassword;

    private JDBCManager() {laodDBConfig();}

    public static JDBCManager getInstance() {
        if (instance == null) {
            instance = new JDBCManager();
        }
        return instance;
    }

    private void laodDBConfig(){
        try{
            Properties prop = new Properties();
            InputStream input = getClass().getResourceAsStream("/db.properties");
            if(input == null){
                System.out.println("nie masz db.properties");
                return;
            }
            prop.load(input);
            dbUrl = prop.getProperty("db.url");
            dbUsername = prop.getProperty("db.username");
            dbPassword = prop.getProperty("db.password");

        }
        catch(Exception e){
            e.printStackTrace();
        }
    }

    public Connection getConnection() throws SQLException {
        if(dbUrl == null || dbUsername == null || dbPassword == null){
            throw new SQLException("nie masz konfigu");
        } else {
            return DriverManager.getConnection(dbUrl, dbUsername, dbPassword);
        }
    }
}
