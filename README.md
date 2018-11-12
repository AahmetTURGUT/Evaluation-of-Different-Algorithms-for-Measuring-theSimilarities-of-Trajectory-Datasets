# Evaluation-of-Different-Algorithms-for-Measuring-theSimilarities-of-Trajectory-Datasets

Çalışmada kullanılan gezinge veri kümesi Geolife projesiadı altında  182 kullanıcı  tarafından beş   yıl baoyunca  (Nisan2007’  den  Ağustos 2012’ye) toplanmıştır. 

Bu  veri   setindekigezingelerin her biri belli zamanlarda ölçülen enlem, boylamve   yükseklik bilgilerinden   oluşmaktadır.Veri   Seti  içerisinde17,621  adet   gezinge   bilgisi   bulunmaktadır.   Bu   gezingeler50,176 saatlik bir   süreçte   toplanmış   ve  toplamda   1,292,951kilometre uzunluğa sahiptir.

Zaman   içerisinde   değişen  konum  verilerden   oluşan   birgezinge ele alındığında, indirgeme işlemi orijinal gezingedeki bazı  noktaları  belirlenen   bir   hata   payı   ile   ihmal  eder  vegezingenin daha az konum verisiyle oluşturulmuş bir benzerini bulmayı   amaçlar.  
Bu   işlem   için   Douglas-Peuckeralgoritması   kullanılmıştır.   Algoritmanın   ana   fikri   verilen gezingedeki   bazı   noktaları  eleyerek  gezingeyi  yaklaşık   birçizgi şeklinde değiştirmektir.

 Daha sonra gezingelerdeki STAYPOİNTler bulunmuştır.  Bu staypointlerden yeni bir gezinge oluşturulmuş boylece gezingenin yaklaşık bir rotası zaman bilgileri ile oluşturulmuştur. Bu noktalar sonrasında KMEANS ile kümelenmiş ve küme sayısını belirlemede BELOW metodu kullanılmıştır. Bu kümelerin merkezleri öklid formulleri ile bulunmuş ve bu noktalardan yeni rota çizilmiştir.

