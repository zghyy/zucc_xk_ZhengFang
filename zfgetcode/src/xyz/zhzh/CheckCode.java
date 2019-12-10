package xyz.zhzh;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

public class CheckCode extends Application {
    private int doneCount = 0;
    private int rightCount = 0;
    private String nowFStr = "";
    private ImageView imgV;
    private Image img;

    public void start(Stage primaryStage) {
        Stage splash = new Stage();

        File f = new File(MySetting.IMG_RESULT);
        File[] files = f.listFiles();

        VBox root = new VBox(5);

        nowFStr = files != null ? files[doneCount].getName() : null;
        String URL = files != null ? files[doneCount].getAbsoluteFile().toURI().toString() : null;
        if (URL != null) {
            img = new Image(URL);
            imgV = new ImageView(img);
            doneCount++;
        }

        Label ocrL = new Label(nowFStr);
        ocrL.setPrefSize(200, 20);
        TextField inputTF = new TextField();
        Label rightL = new Label("Correct: 0.00");

        root.getChildren().addAll(imgV, ocrL, inputTF, rightL);
        root.setOnKeyPressed(event -> {
            if (event.getCode() == KeyCode.ENTER) {
                String name = inputTF.getText();
                File file = new File(MySetting.IMG_RESULT + nowFStr);
                if (name == null || name.equals("")) {
                    rightCount++;
                    final boolean delete = file.delete();
                    if (!delete) {
                        System.out.println("删除正确文件失败");
                    }
                } else {
                    inputTF.setText("");
                    File aimA = new File("./data/wrong/" + name + ".gif");
                    // 修正的文件
                    File aimB = new File("./data/wrongOrg/" + nowFStr);
                    // 错误的原始文件
                    try {
                        Files.copy(file.toPath(), aimA.toPath());
                        Files.copy(file.toPath(), aimB.toPath());
                        final boolean delete = file.delete();
                        if (!delete) {
                            System.out.println("删除错误文件失败");
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }

                System.out.println(
                        "Total: " + doneCount + "\tRight: " + rightCount + "\tWrong: " + (doneCount - rightCount));
                rightL.setText("Correct: " + (1.0 * rightCount / doneCount));

                assert files != null;
                nowFStr = files[doneCount].getName();
                String URL1 = files[doneCount].getAbsoluteFile().toURI().toString();
                img = new Image(URL1);
                imgV.setImage(img);
                ocrL.setText(nowFStr);
                doneCount++;
            }
        });

        Scene scene = new Scene(root);
        splash.setScene(scene);
        splash.setTitle("Src");
        splash.show();

    }

    public static void main(String[] args) {
        Application.launch(args);
    }
}
