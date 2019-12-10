package xyz.zhzh;

import java.io.File;
import java.io.FileOutputStream;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.io.IOException;

class getCodeIMG {
    static void main() throws IOException {
        System.out.println("当前单次爬取数量为：" + MySetting.count);
        for (int i = 0; i < MySetting.count; i++) {
            HttpGet secretCodeGet = new HttpGet(MySetting.SECRETE_URL);
            CloseableHttpClient client = HttpClients.createDefault();
            CloseableHttpResponse responseSecret = client.execute(secretCodeGet);
            FileOutputStream fileOutputStream = new FileOutputStream(new File(MySetting.IMG_DOWN + "Code" + i + ".gif"));
            responseSecret.getEntity().writeTo(fileOutputStream);
            fileOutputStream.close();
            System.out.println("Code" + i + ".gif ");
        }
        System.out.println("Finish!");
    }
}
