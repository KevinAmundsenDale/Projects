var Cube = [[0,0,0,4,4,4,0,0,0],
            [0,0,0,4,4,4,0,0,0],
            [0,0,0,4,4,4,0,0,0],
            [2,2,2,1,1,1,3,3,3],
            [2,2,2,1,1,1,3,3,3],
            [2,2,2,1,1,1,3,3,3],
            [0,0,0,5,5,5,0,0,0],
            [0,0,0,5,5,5,0,0,0],
            [0,0,0,5,5,5,0,0,0],
            [0,0,0,6,6,6,0,0,0],
            [0,0,0,6,6,6,0,0,0],
            [0,0,0,6,6,6,0,0,0]]

//          oransj = 4
// grønn = 2 white = 1 blå = 3
//          rød = 5
//          gul = 6

var scrambledCube = Cube;

function R(arr) {
    for(i = 0; i < 3; i++){
        [scrambledCube[2-i][5], scrambledCube[5-i][5]] = [scrambledCube[5-i][5], scrambledCube[2-i][5]];
        [scrambledCube[11-i][5], scrambledCube[5-i][5]] = [scrambledCube[5-i][5], scrambledCube[11-i][5]];
        [scrambledCube[8-i][5], scrambledCube[5-i][5]] = [scrambledCube[5-i][5], scrambledCube[8-i][5]];

        [scrambledCube[3+i][7+(i%2)], scrambledCube[4][6]] = [scrambledCube[4][6], scrambledCube[3+i][7+(i%2)]];
        [scrambledCube[3+(2*i**2)%6][8+i*(((3*i)%2)-1)], scrambledCube[3][6]] = [scrambledCube[3][6], scrambledCube[3+(2*i**2)%6][8+i*(((3*i)%2)-1)]];
    }
}

function L(arr) {
    for(i = 0; i < 3; i++){
        [scrambledCube[0+i][3], scrambledCube[3+i][3]] = [scrambledCube[3+i][3], scrambledCube[0+i][3]];
        [scrambledCube[9+i][3], scrambledCube[3+i][3]] = [scrambledCube[3+i][3], scrambledCube[9+i][3]];
        [scrambledCube[6+i][3], scrambledCube[3+i][3]] = [scrambledCube[3+i][3], scrambledCube[6+i][3]];

        [scrambledCube[3+i][1+(i%2)], scrambledCube[4][0]] = [scrambledCube[4][0], scrambledCube[3+i][1+(i%2)]];
        [scrambledCube[3+(2*i**2)%6][2+i*(((3*i)%2)-1)], scrambledCube[3][0]] = [scrambledCube[3][0], scrambledCube[3+(2*i**2)%6][2+i*(((3*i)%2)-1)]];
    }
}

function U(arr) {
    for(i = 0; i < 3; i++){
        [scrambledCube[3+i][6], scrambledCube[2][3+i]] = [scrambledCube[2][3+i], scrambledCube[3+i][6]];
        [scrambledCube[6][5-i], scrambledCube[2][3+i]] = [scrambledCube[2][3+i], scrambledCube[6][5-i]];
        [scrambledCube[5-i][2], scrambledCube[2][3+i]] = [scrambledCube[2][3+i], scrambledCube[5-i][2]];
        
        [scrambledCube[3+i][4+(i%2)], scrambledCube[4][3]] = [scrambledCube[4][3], scrambledCube[3+i][4+(i%2)]];
        [scrambledCube[3+(2*i**2)%6][5+i*(((3*i)%2)-1)], scrambledCube[3][4]] = [scrambledCube[3][4], scrambledCube[3+(2*i**2)%6][5+i*(((3*i)%2)-1)]];
    }
}

function D(arr) {
    for(i = 0; i < 3; i++){
        [scrambledCube[3+i][0], scrambledCube[0][5-i]] = [scrambledCube[0][5-i], scrambledCube[3+i][0]];
        [scrambledCube[8][3+i], scrambledCube[0][5-i]] = [scrambledCube[0][5-i], scrambledCube[8][3+i]];
        [scrambledCube[5-i][8], scrambledCube[0][5-i]] = [scrambledCube[0][5-i], scrambledCube[5-i][8]];

        [scrambledCube[3+i][4+(i%2)], scrambledCube[4][3]] = [scrambledCube[4][3], scrambledCube[3+i][4+(i%2)]];
        [scrambledCube[3+(2*i**2)%6][5+i*(((3*i)%2)-1)], scrambledCube[3][4]] = [scrambledCube[3][4], scrambledCube[3+(2*i**2)%6][5+i*(((3*i)%2)-1)]];
    }
}

function F(arr) {
    for(i = 0; i < 3; i++){
        [scrambledCube[5][6+i], scrambledCube[5][3+i]] = [scrambledCube[5][3+i], scrambledCube[5][6+i]];
        [scrambledCube[9][5-i], scrambledCube[5][3+i]] = [scrambledCube[5][3+i], scrambledCube[9][5-i]];
        [scrambledCube[5][0+i], scrambledCube[5][3+i]] = [scrambledCube[5][3+i], scrambledCube[5][0+i]];

        [scrambledCube[9+i][4+(i%2)], scrambledCube[10][6]] = [scrambledCube[11][6], scrambledCube[9+i][4+(i%2)]];
        [scrambledCube[9+(2*i**2)%6][5+i*(((3*i)%2)-1)], scrambledCube[9][4]] = [scrambledCube[9][4], scrambledCube[9+(2*i**2)%6][5+i*(((3*i)%2)-1)]];
    }
}

function B(arr) {
    for(i = 0; i < 3; i++){
        [scrambledCube[3][2-i], scrambledCube[3][5-i]] = [scrambledCube[3][5-i], scrambledCube[3][2-i]];
        [scrambledCube[11][3+i], scrambledCube[3][5-i]] = [scrambledCube[3][5-i], scrambledCube[11][3+i]];
        [scrambledCube[3][8-i], scrambledCube[3][5-i]] = [scrambledCube[3][5-i], scrambledCube[3][8-i]];

        [scrambledCube[0+i][4-(i%2)], scrambledCube[1][5]] = [scrambledCube[1][5], scrambledCube[0+i][4-(i%2)]];
        [scrambledCube[0+(2*i**2)%6][3-i*(((3*i)%2)-1)], scrambledCube[0][5]] = [scrambledCube[0][5], scrambledCube[0+(2*i**2)%6][3-i*(((3*i)%2)-1)]];
    }
}

function Rprime(arr){R(arr),R(arr),R(arr)}

function Lprime(arr){L(arr),L(arr),L(arr)}

function Uprime(arr){U(arr),U(arr),U(arr)}

function Dprime(arr){D(arr),D(arr),D(arr)}

function Fprime(arr){F(arr),F(arr),F(arr)}

function Bprime(arr){B(arr),B(arr),B(arr)}



Rprime(scrambledCube);
console.log(scrambledCube);