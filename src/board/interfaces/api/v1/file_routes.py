from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from board.application.file.file_dto import FileResponseDTO
from board.application.file.file_service import FileApplicationService
from board.domain.user.user import User
from ..dependencies import get_file_service, get_current_user

router = APIRouter()


@router.post("/upload/{post_id}", response_model=FileResponseDTO)
async def upload_file(
        post_id: int,
        file: UploadFile = File(...),
        file_service: FileApplicationService = Depends(get_file_service),
        current_user: User = Depends(get_current_user),
):
    return await file_service.save_file(file, post_id)


@router.get("/post/{post_id}", response_model=list[FileResponseDTO])
def get_files_by_post(
        post_id: int, file_service: FileApplicationService = Depends(get_file_service)
):
    return file_service.get_files_by_post(post_id)


@router.delete("/{file_id}")
def delete_file(
        file_id: int,
        file_service: FileApplicationService = Depends(get_file_service),
        current_user: User = Depends(get_current_user),
):
    try:
        file_service.delete_file(file_id)
        return {"message": "File deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
