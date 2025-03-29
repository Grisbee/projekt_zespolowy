package ex00;

import ex00.database.GetDatabaseData;
import ex00.database.JDBCManager;

import java.sql.Connection;

public class Main {
    public static void main(String[] args) {
        Connection con = null;
        GetDatabaseData getDatabaseData = new GetDatabaseData();
        try {

            Class.forName("org.postgresql.Driver");
            con = JDBCManager.getInstance().getConnection();
            if (con != null) {
                System.out.println("Connection established");
                getDatabaseData.getDBData(con);
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
