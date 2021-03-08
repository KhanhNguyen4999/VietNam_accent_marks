
function view_list(arr, coor_x, coor_y){   // Thêm truy vết vào 
    // Hiển thị table
    content = `<table id = "table" width="80%" border = "1" cellpadding = "5" cellspacing = "5">`
    for(i=0;i<coor_x;i++){
        var element = `<tr class=row_${i}>`;
        for(j=0;j<coor_y;j++){
            element+=`<th id = "${i},${j}" >${arr[i][j]}</th>`
        }
        element += "</tr>"
        content+=element;
    }
    content +='</table>'
    return content;
}

function backrace_view(backtrace, m, n, str1, str2){
    //
    var forwardPath = []; 
    var x, pos_x, pos_y, pos_xy
    ;
    // Color the cell at (m,n)
    var s = `${m},${n}`;
    forwardPath.push(s);
    x = document.getElementById(`${s}`);
    x.style.backgroundColor = "yellow";

    // get all values on backtrace
    ds_values = Object.values(backtrace);
    var parent = backtrace[s];
    // end_path = ["1,1", "2,1", "1,2"];

    while(parent){
        css_id = `${parent.x},${parent.y}`;
        forwardPath.push(css_id);
        parent = backtrace[css_id];
        x = document.getElementById(`${css_id}`);
        x.style.backgroundColor = "yellow";
    }
    // case length of string 2 more than length of string 1
    if(!["1,1", "2,1", "1,2"].includes(css_id)){
        pos_xy = css_id.split(",");
        pos_x = parseInt(pos_xy[0]);
        pos_y = parseInt(pos_xy[1]);
        if (pos_x==1){
            pos_y -= 1;
            while(pos_y != 1){
                css_id = `${pos_x},${pos_y}`;
                forwardPath.push(css_id);
                x = document.getElementById(css_id);
                x.style.backgroundColor = "yellow";
                pos_y -=1;
            }
        }
        else{
            pos_x -= 1;
            while(pos_x != 1){
                css_id = `${pos_x},${pos_y}`;
                forwardPath.push(css_id);
                x = document.getElementById(css_id);
                x.style.backgroundColor = "yellow";
                pos_x -=1;
            }
        }
    }

    //color the cell at (2,2)
    x = document.getElementById("1,1");
    x.style.backgroundColor = "yellow";
    forwardPath.push('1,1');
    forwardPath.reverse();

    var array_str1 = [];
    var array_str2 = []
    console.log(forwardPath);
    for(var i = 0;i<forwardPath.length-1;i++){
        pos_str1 = forwardPath[i].split(',');
        pos_str2=  forwardPath[i+1].split(',');

        pos_x1 = parseInt(pos_str1[0]);
        pos_y1 = parseInt(pos_str1[1]);
        // console.log(pos_x1, pos_y1)
        
        pos_x2 = parseInt(pos_str2[0]);
        pos_y2 = parseInt(pos_str2[1]);
        // console.log(pos_x2, pos_y2);

        if(pos_x2 > pos_x1 & pos_y2 > pos_y1){
            array_str1.push(str1[pos_x2-2]);
            array_str2.push(str2[pos_y2-2]);
        }
        else if(pos_x2>pos_x1){
            array_str1.push(str1[pos_x2-2]);
            array_str2.push("*");
        }
        else{
            array_str1.push("*");
            array_str2.push(str2[pos_x2-2]);
        }
    }
    console.log(array_str1);
    console.log(array_str2);


    element = '<p text-align:center; margin-top:50px> Two  Strings and their alignment</p>';

    element += `<table id = "table" width="80%" border = "1" cellpadding = "5" cellspacing = "5">`

    element += "</tr>"
    for(j=0;j<array_str1.length;j++){
        element+=`<th>${array_str1[j]}</th>`
    }
    element += "</tr>"
    for(j=0;j<array_str1.length;j++){
        element+=`<th>|</th>`
    }
    element += "</tr>"
    for(j=0;j<array_str1.length;j++){
        element+=`<th>${array_str2[j]}</th>`
    }
        
    element +='</table>'
    $("#main_table").append(element);
}

function make_beautiful(m, n){
    var x;
    for(var i=0; i<m; i++){
        for(var j=0; j<n; j++){
            if(j == 0){ // make color for first column
                console.log(j)
                x = document.getElementById(`${i},${j}`);
                x.style.backgroundColor = "coral";
                x.style.fontWeight = "bolder";
                x.style.fontStyle = "italic";
                x.style.color = "Cyan"
            }
            if(i==0){ // make color for fist row
                x = document.getElementById(`${i},${j}`);
                x.style.backgroundColor = "coral";
                x.style.fontWeight = "bolder";
                x.style.fontStyle = "italic";
                x.style.color = "Cyan"
            }
        }
    }
}


function getString(){
    // Get value of 2 string
    var str1 = document.getElementById("str_1").value;
    var str2 = document.getElementById("str_2").value;

    var str1_len = str1.length ;
    var str2_len = str2.length ;

    // initiate array
    var i, j;
    stride = 2
    coor_x = str1_len+stride; // number of rows
    coor_y = str2_len+stride; // number of cols

    let arr = new Array(coor_x); // create an empty array of length n
    for (i = 0; i < coor_x; i++) {
        arr[i] = new Array(coor_y); // make each element an array
        for(j = 0; j <coor_y; j++){
            arr[i][j] = 0
        }
    }
    //
    for(i=2;i<coor_x;i++){
        arr[i][0] = str1[i-2]
        arr[i][1] = i-1
    }
    //
    for(i=2;i<coor_y;i++){
        arr[0][i] = str2[i-2]
        arr[1][i] = i-1
    }

    // Tính edit distance
    var val, ls_pos, x, y;
    var backtrace = {}; // Lưu lại đường đi
    for(i=2;i<coor_x;i++){
        for(j=2;j<coor_y;j++){
            diff = (str1[i-2] == str2[j-2]) ? 0 : 2;
            console.log(arr[i-1][j]+1,  arr[i][j-1]+1, arr[i-1][j-1]+ diff, diff);
            ls_pos = [arr[i-1][j-1]+ diff, arr[i-1][j]+1,  arr[i][j-1]+1];
            v_min = Math.min(...ls_pos);
            index_corresp =  ls_pos.indexOf(v_min);
            
            var obj_parent = {};
            if (index_corresp == 0){
                x = i-1;
                y = j-1;
            }
            else if (index_corresp==1){
                x = i-1;
                y = j;
            }
            else{
                x = i;
                y = j-1;
            }
            obj_parent.x = x;
            obj_parent.y = y;

            var key = `${i},${j}`;
            backtrace[key]= obj_parent;
            arr[i][j] = v_min;
        }
    }

    // Print table
    $("#main_table").html("");
    content = view_list(arr, coor_x, coor_y);
    $("#main_table").append(content);
    // outside decoration for table
    make_beautiful(coor_x, coor_y);

    backrace_view(backtrace, coor_x-1, coor_y-1, str1, str2);
}