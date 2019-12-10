package xyz.zhzh;

import javax.imageio.ImageIO;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

public class PNGtogif {
    public static void main(String[] args) throws IOException{
        File f = new File(MySetting.MODEL);
        File[] files = f.listFiles();
        if (files != null) {
            for (File file : files) {
                String filename = file.getName().substring(0, (file.getName().length()-3)) + "gif";
                OutputStream out = new FileOutputStream(MySetting.MODEL +
                        filename);
                ImageIO.write(ImageIO.read(file), "gif", out);
                out.close();
                if (!file.delete())
                {
                    System.out.println("删除失败！");
                }
                System.out.println(filename);
            }
        }
    }
}
