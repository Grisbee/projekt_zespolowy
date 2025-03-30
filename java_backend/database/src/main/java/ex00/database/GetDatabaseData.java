package ex00.database;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class GetDatabaseData {
    public void getDBData(Connection connection) throws SQLException {
        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("select * from products");
        int recordCount = 0;
        while(resultSet.next()){
            //product_id, title, description, price, url, product_source, currency
            System.out.println(resultSet.getInt("product_id") + "\t" + resultSet.getString("title") + "\t" + resultSet.getString("description") + "\t" + resultSet.getFloat("price")
            + "\t" + resultSet.getString("url") + "\t" + resultSet.getString("product_source") + "\t" + resultSet.getString("currency") + "\t" + resultSet.getFloat("rating") + "\t" + resultSet.getInt("review_count"));
            recordCount++;
        }
        resultSet.close();
        statement.close();
    }
}
