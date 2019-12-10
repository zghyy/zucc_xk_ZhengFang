package xyz.zhzh;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws Exception {
        Scanner in = new Scanner(System.in);
        label:
        do {
            System.out.println("请输入要执行的操作：\n1.爬取数据集\n2.处理数据集\n" +
                    "3.人工检查数据集\n4.识别验证码\n输入任意其他字符即可退出");
            String cmd = in.nextLine();
            switch (cmd) {
                case "1":
                    getCodeIMG.main();
                    break;
                case "2":
                    CodeProcess.main();
                    break;
                case "3":
                    CheckCode.main(args);
                    break;
                case "4":
                    String result = CodeProcess.getAllOcr("./code.gif");
                    System.out.println(result);
                    break;
                default:
                    break label;
            }
        } while (true);

    }
}
