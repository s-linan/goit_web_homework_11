from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, or_, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact
from src.schemas.contact import ContactSchema, ContactUpdate


async def search_contacts_by(db: AsyncSession, first_name: Optional[str] = None,
                             last_name: Optional[str] = None,
                             email: Optional[str] = None):
    stmt = select(Contact).filter(
        or_(Contact.first_name == first_name, Contact.last_name == last_name, Contact.email == email))
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contacts_with_birthdays(db: AsyncSession):
    current_date = datetime.now().date()
    seven_days_ahead = current_date + timedelta(days=7)
    seven_days_ahead_day = func.extract('day', seven_days_ahead)
    seven_days_ahead_month = func.extract('month', seven_days_ahead)
    current_day = func.extract('day', current_date)
    current_month = func.extract('month', current_date)
    stmt = select(Contact).filter(
        extract('month', Contact.birthday).between(current_month, seven_days_ahead_month) & (
            extract('day', Contact.birthday).between(current_day, seven_days_ahead_day)))
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        for key, value in body.dict(exclude_unset=True).items():
            setattr(contact, key, value)
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
