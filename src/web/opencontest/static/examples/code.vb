Module Module1
    Private n As Integer
    Private i as Integer

    Sub Main()
        n = Convert.toInt32(Console.ReadLine())
        for i = 0 to n - 1
            Console.WriteLine(i)
        next i
    End Sub
End Module