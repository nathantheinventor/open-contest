using System;
 
public class HelloWorld {
    static public void Main () {
        int n = Convert.ToInt32(Console.ReadLine());
        for (int i = 0; i < n; i ++) {
            Console.WriteLine(i);
        }
    }
}