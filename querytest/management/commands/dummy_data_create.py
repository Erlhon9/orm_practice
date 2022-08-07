import string
import time
from typing import Any, Optional
from random import randint, choice
from django.core.management import BaseCommand
from django.db import transaction, IntegrityError, DatabaseError
from django.utils import timezone

from querytest.models import Product, ProductAttr, Stock, StockBox, StockBoxItem

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        DUMMY_CREATED = False
        product_cnt = 10
        attr_type = 2
        stock_cnt = 5
        stock_box_cnt = 10
        
        sizes = ['S', 'M', 'L', '85', '90', '95', '100', '105', 'Free']
        style = ['skirt', 'pants', 'shirts', 'shoes', 'bag', 'accessory', 'etc']
        
        try:
            with transaction.atomic():
                start = time.time()
                Product.objects.bulk_create([
                    Product(
                        name=f'product__{idx}',
                        price=randint(1000, 100000),
                    ) for idx in range(product_cnt)
                ])
                
                product_ids = Product.objects.all().values('id')
                end = time.time()
                self.stdout.write(self.style.SUCCESS('Product 생성 완료 🔥 : {:.2f}s'.format(end - start)))
                start = end
                
                for _ in range(attr_type):
                    ProductAttr.objects.bulk_create([
                        ProductAttr(
                            product=Product.objects.get(id=idx['id']),
                            sizes=sizes[randint(0,(len(sizes)-1))],
                            style=style[randint(0,(len(style)-1))],
                        ) for idx in product_ids
                    ])
                
                end = time.time()
                print(self.style.SUCCESS('ProductAttr 생성 완료 🔥 : {:.2f}s'.format(end - start)))
                start = end
                
                product_attr_ids = ProductAttr.objects.all().values('id')
                
                for _ in range(stock_cnt):
                    Stock.objects.bulk_create([
                        Stock(
                            product_attr=ProductAttr.objects.get(id=idx['id']),
                            code=''.join(choice(string.ascii_lowercase+string.digits) for _ in range(10))
                        ) for idx in product_attr_ids
                    ])
                    
                end = time.time()
                print(self.style.SUCCESS('Stock 생성 완료 🔥 : {:.2f}s'.format(end - start)))
                start = end
                
                StockBox.objects.bulk_create([
                    StockBox(
                        address=f'address_{idx}',
                        created_time=timezone.now(),
                    ) for idx in range(stock_box_cnt)
                ])
                
                end = time.time()
                print(self.style.SUCCESS('StockBox 생성 완료 🔥 : {:.2f}s'.format(end - start)))
                start = end
                
                stock_ids = Stock.objects.all().values('id')
                stock_box_ids = StockBox.objects.all().values('id')
                for i in stock_ids:
                    StockBoxItem.objects.bulk_create([
                        StockBoxItem(
                            stock=Stock.objects.get(id=i['id']),
                            stock_box=StockBox.objects.get(id=idx['id']),
                        ) for idx in stock_box_ids
                    ])
                    
                end = time.time()
                print(self.style.SUCCESS('StockBoxItem 생성 완료 🔥 : {:.2f}s'.format(end - start)))
                start = end    
                
                DUMMY_CREATED = True
                
        except IntegrityError as Error:
            self.stderr.write(self.style.ERROR(f'더미 데이터 생성 실패: Integrity 😥\n {Error}'))
        except DatabaseError as Error:
            self.stderr.write(self.style.ERROR(f'더미 데이터 생성 실패: database 😥\n {Error}'))
        except Exception as Error:
            self.stderr.write(self.style.ERROR(f'더미 데이터 생성 실패: 😥\n {Error}'))
            
        
        if DUMMY_CREATED:
            self.stdout.write(self.style.SUCCESS('더미 데이터 생성 완료 🔥'))