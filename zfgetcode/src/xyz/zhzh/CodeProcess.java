package xyz.zhzh;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.nio.file.Files;
import java.util.*;
import java.util.List;

class CodeProcess {
    private static Map<BufferedImage, String> trainMap = null;
    private static int index = 0;

    static void main() throws Exception {
        Scanner in = new Scanner(System.in);
        System.out.println("输入1开始用当前模型处理数据集，输入2表示根据当前数据集生成模型，输入其他数字返回");
        int choice = in.nextInt();
        if (choice == 1){
            startOCR();
            System.out.println("识别完成");
        }
        else if (choice == 2) {
            trainModel();
            System.out.println("模型生成完毕");
        }
    }

    /*
     * 生成字模入口
     */
    private static void trainModel() throws Exception {
        File dir = new File(MySetting.IMG_RESULT);
        File[] files = dir.listFiles();
        if (files != null) {
            for (File file : files) {
                BufferedImage img = removeBackgroud(MySetting.IMG_RESULT + file.getName());
                List<BufferedImage> listImg = splitImage(img);
                if (listImg.size() == 4) {
                    for (int j = 0; j < listImg.size(); j++) {
                        ImageIO.write(listImg.get(j), "gif",
                                new File(MySetting.MODEL + file.getName().charAt(j) + "-" + (index++) + ".gif"));
                        System.out.println(file.getName() + "\t" + file.getName().charAt(j) + "-" + (index++) + ".gif");
                    }
                }
            }
        }
    }

    private static void startOCR() throws Exception {
        int sameCount = 0;
        for (int i = 0; i < MySetting.count; i++) {
            String resultStr = getAllOcr(MySetting.IMG_DOWN + "Code" + i + ".gif");
            System.out.println(i + ".gif = " + resultStr);
            File source = new File(MySetting.IMG_DOWN + "Code" + i + ".gif");
            File dest = new File(MySetting.IMG_RESULT + resultStr + ".gif");
            if (dest.exists()) {
                sameCount++;
            } else {
                Files.copy(source.toPath(), dest.toPath());
//                if (!source.delete())
//                    System.out.println("删除文件失败！");
            }
        }
        System.out.println("重复验证码有：" + sameCount);
    }

    /*
     * 识别验证码
     */
    static String getAllOcr(String file) throws Exception {
        BufferedImage img = removeBackgroud(file);
        List<BufferedImage> listImg = splitImage(img);
        Map<BufferedImage, String> map = loadModelData();
        if (map == null) {
            return null;
        }
        StringBuilder result = new StringBuilder();
        for (BufferedImage bIMG : listImg) {
            result.append(getSingleCharOcr(bIMG, map));
        }
        return result.toString();
    }

    /*
     * 因为四个字符的颜色均为纯蓝色，所以通过把图片蓝色设置为黑色，其他所有颜色设置为白色来把图片二值化并去噪
     */
    private static BufferedImage removeBackgroud(String picFile) throws Exception {
        BufferedImage img = ImageIO.read(new File(picFile));
        int width = img.getWidth();
        int height = img.getHeight();
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (isBlue(img.getRGB(x, y)) == 1) {
                    img.setRGB(x, y, Color.BLACK.getRGB());
                } else {
                    img.setRGB(x, y, Color.WHITE.getRGB());
                }
            }
        }
        return img;
    }

    /*
     * 因为所有验证码都是蓝色的
     */
    private static int isBlue(int colorInt) {
        Color color = new Color(colorInt);
        int rgb = color.getRed() + color.getGreen() + color.getBlue();
        if (rgb == 153) {
            return 1;
        }
        return 0;
    }

    /*
     * 切割验证码图片
     */
    private static List<BufferedImage> splitImage(BufferedImage img){
        List<BufferedImage> subImgs = new ArrayList<>();
        subImgs.add(img.getSubimage(5, 0, 12, 23));
        subImgs.add(img.getSubimage(17, 0, 12, 23));
        subImgs.add(img.getSubimage(29, 0, 12, 23));
        subImgs.add(img.getSubimage(41, 0, 12, 23));
        return subImgs;
    }

    private static Map<BufferedImage, String> loadModelData() throws Exception {
        if (trainMap == null) {
            Map<BufferedImage, String> map = new HashMap<>();
            File dir = new File(MySetting.MODEL_ROOT);
            File[] files = dir.listFiles();
            if (files == null) {
                System.out.println(dir.getName() + "下没有字模！");
                return null;
            }
            for (File file : files) {
                map.put(ImageIO.read(file), file.getName().charAt(0) + "");
            }
            trainMap = map;
        }
        return trainMap;
    }

    /*
     * 识别切割的单个字符
     */
    private static String getSingleCharOcr(BufferedImage img, Map<BufferedImage, String> map) {
        String result = "#";
        int width = img.getWidth();
        int height = img.getHeight();
        int min = width * height;
        for (BufferedImage bi : map.keySet()) {
            int count = 0;
            if (Math.abs(bi.getWidth() - width) > 2)
                continue;
            int widthmin = width < bi.getWidth() ? width : bi.getWidth();
            int heightmin = height < bi.getHeight() ? height : bi.getHeight();
            Label1: for (int x = 0; x < widthmin; ++x) {
                for (int y = 0; y < heightmin; ++y) {
                    if (isBlack(img.getRGB(x, y)) != isBlack(bi.getRGB(x, y))) {
                        count++;
                        if (count >= min)
                            break Label1;
                    }
                }
            }
            if (count <= 3) {
                result = map.get(bi);
                break;
            }
            else if (count < min) {
                min = count;
                result = map.get(bi);
            }
        }
        return result;
    }

    /*
     * 识别已被处理成黑色的字符
     */
    private static int isBlack(int colorInt) {
        Color color = new Color(colorInt);
        if (color.getRed() + color.getGreen() + color.getBlue() <= 100) {
            return 1;
        }
        return 0;
    }
}
