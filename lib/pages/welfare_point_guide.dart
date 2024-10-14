import 'package:flutter/material.dart';

class WelFarePoint extends StatelessWidget {
  const WelFarePoint({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 235, 231, 231),
      appBar: AppBar(
        title: const Text('복지포인트 잔액', style: TextStyle(fontFamily: 'PretendardLight'),),
        centerTitle: true,
        backgroundColor: Color.fromARGB(255, 235, 231, 231),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            SizedBox(
              height: 20.0,
              ),
            Container(
              padding: EdgeInsets.fromLTRB(0.0, 10.0, 0.0, 0.0),
              width: 380,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10.0),
                color: Color.fromARGB(255, 255, 255, 255)
              ),
              child: Column(
                children: <Widget>[
                  SizedBox(
                    height: 10.0,
                  ),  
                  Text('잔여포인트 : 1,400,000', style: TextStyle(fontFamily: 'PretendardBold',
                  fontSize: 18.0),
                  textAlign: TextAlign.left,
                  ),
                  SizedBox(
                    height: 20.0,
                  ),
                  Container(
                    height: 10.0,
                    width: 330.0,
                    decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10.0),
                    color: Color.fromARGB(255, 212, 208, 208)
                    ),
                    child: Container(
                      width: 10,
                      margin: EdgeInsets.fromLTRB(0.0, 0.0, 40.0, 0.0),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10.0),
                        color: Color.fromARGB(255, 80, 120, 194),
                      ),
                    ),
                  ),
                  Row(children: <Widget>[
                    SizedBox(
                      height: 50.0,
                    ),
                    Container(
                      width: 70.0,
                      height: 10.0,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Color.fromARGB(255, 80, 120, 194),
                      ),
                    ),
                    Text('사용포인트             3,400,000', style: TextStyle(fontFamily: 'PretendardBold')),
                    SizedBox(
                      height: 10.0,
                    ),
                  ],
                  ),
                  Row(children: <Widget>[
                    SizedBox(
                      height: 20.0,
                    ),
                    Container(
                      width: 70.0,
                      height: 10.0,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Color.fromARGB(255, 212, 208, 208),
                      ),
                    ),
                    Text('총 배정포인트        4,800,000', style: TextStyle(fontFamily: 'PretendardBold')),
                  ],
                  ),
                  SizedBox(
                      height: 20.0,
                    ),
                ],
              ),
            ),
            Container(
              child: Column(
                children: <Widget>[
                  SizedBox(
                    height: 50,
                  ),
                  Container(
                    width: 330.0,
                    decoration: BoxDecoration(
                      color: Color.fromARGB(255, 255, 255, 255),
                      border: Border.all(color: Color.fromARGB(255, 38, 72, 146), width: 3),
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                    child:  Text('실적 충족 여부 : 충족', style: TextStyle(fontFamily: 'PretendardSemiBold',
                  fontSize: 15.0),
                  textAlign: TextAlign.center,
                  )
                  ),
                   SizedBox(
                    height: 20,
                  ),
                  InkWell(
                    onTap: () {
                      print('조회페이지로 이동');
                      },
                      child: Container(
                    width: 330.0,
                    decoration: BoxDecoration(
                      color: Color.fromARGB(255, 38, 72, 146),
                      border: Border.all(color: Color.fromARGB(255, 38, 72, 146), width: 3),
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                    child:  Text('복지포인트 사용내역 조회', style: TextStyle(fontFamily: 'PretendardSemiBold',
                  fontSize: 15.0,
                  color: Color.fromARGB(255, 255, 255, 255)),
                  textAlign: TextAlign.center,
                  )
                  ),
                  ),
                ],
              )
            )
          ],
        )
      ),
    );
  }
}