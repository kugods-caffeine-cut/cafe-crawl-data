var fs = require('fs');
const _ = require("lodash");
require("dotenv").config();
const { connect } = require('./config/mongoose');
const { Drink } = require('./model/Drink')


/**
 * DB 연결
 */
connect();

/**
 * 파일 이름을 입력받아 커피 브랜드를 문자열로 반환합니다.
 * @type { (filename : string) => string }
 */
const getName = (filename) => {
    brand = ""
    brand_map = {
        "starbucks": "스타벅스",
        "coffeebean": "커피빈",
        "compose": "컴포즈커피",
        "ediya": "이디야",
        "hollys": "할리스",
        "megacoffee": "메가커피",
        "tomntoms": "탐앤탐스",
        "twosome": "투썸플레이스"
    };
    for (var key in brand_map) {
        if (filename.includes(key)) {
            brand = brand_map[key]
        }
    }
    return brand
}

/** @type {Array<{ brand: string ,drink_name: string, temp: string, img: string, size: number, kcal: number, caffeine: number }>} */
let items = [];
var files = fs.readdirSync('../drink-data/');

/**
 * ../drink-data/ 폴더 안의 파일들을 순회하여 음료데이터에 brand 필드를 추가한 후, items에 음료를 추가한다.
 */
for (idx in files) {
    let obj = JSON.parse(fs.readFileSync('../drink-data/' + files[idx], 'utf8'));
    const brand = getName(files[idx]);
    let temp = _.cloneDeep(obj)
    temp['item'].map(elem => {
        elem["brand"] = brand;
        return elem
    });

    items = items.concat(temp['item']);
}

/**
 * DB controller 함수 정의 예시
 */

// items를 wrapping하여 BulkWrite 쿼리 작성
// drink_name / brand / temp 기준으로 upsert 판단하여 commit
for (let i in items) {
    items[i] = {
        updateOne: {
            filter: { drink_name: items[i].drink_name, brand: items[i].brand, temp: items[i].temp },
            update: items[i],
            upsert: true
        }
    }
}

foo = async () => {
    const res = await Drink.bulkWrite(items)
    console.log(res)
}

// foo();