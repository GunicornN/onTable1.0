import psycopg2
import psycopg2.extensions
import random

conn = psycopg2.connect("dbname=ontable user=alexisdubanchet password=password host=127.0.0.1")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

items_per_order = range(1, 5)
num_orders = 10
companyId = 1


def getRandomElemFromArray(array):
    if len(array) == 0:
        return 0
    rnd = random.randint(0, len(array) - 1)
    return array[rnd]

def gatherData(request):
    cur = conn.cursor()
    cur.execute(request)
    items_todo = cur.fetchall()
    items = []
    for item in items_todo:
        items.append(item[0])
    cur.close()
    return items

def main():
    cur = conn.cursor()
    cur.execute("TRUNCATE company_cart CASCADE;")
    conn.commit()

    products = gatherData("SELECT id FROM company_product WHERE available = true;")
    companys = gatherData("SELECT id FROM company_company;")
    tables = gatherData("SELECT id FROM company_table;")

    companys = [1]

    print(products)
    print(companys)
    print(tables)

    cur = conn.cursor()
    for comm in range(num_orders):
        #{getRandomElemFromArray(companys)},

        # Insert into cart
        companyCartInsert = f"""
            INSERT INTO 
            company_cart(
            person_name, 
            total_amount,
            paid_amount,
            discount,
            payment_method,
            created_on,
            paid_on,
            company_id,
            table_id
            ) VALUES (
            'filler',
            {random.randint(0, 20)},
            {random.randint(0, 20)},
            0,
            'CB',
            current_timestamp,
            current_timestamp,
            {companyId},
            {getRandomElemFromArray(tables)}
            ) RETURNING id;
            """
        cur.execute(companyCartInsert)
        idcart = cur.fetchone()[0]
        # Insert into cart items
        for item_counter in items_per_order:
            plat = f"""
            INSERT INTO
            company_cart_items(
            price,
            vat,
            cart_id,
            formulas_id,
            items_id
            ) VALUES (
            {random.randint(0, 20)},
            0,
            {idcart},
            null,
            (SELECT id FROM company_product WHERE company_id = {companyId} ORDER BY RANDOM() LIMIT 1)
            );
            """
            cur.execute(plat)
            print(item_counter)
    conn.commit()


if __name__ == "__main__":
    main()