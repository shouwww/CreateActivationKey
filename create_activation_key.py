import wmi
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64


def get_volume_serial_number():
    """
    実行しているPCのCドライブのボリュームシリアルナンバーを取得する。

    Parameters
    ----------
    None

    Returns
    -------
    ret_VolumeSerialNumber : str
        実行しているPCのCドライブのボリュームシリアルナンバー。
    """

    ret_VolumeSerialNumber = ""
    tmp_wmi = wmi.WMI()
    try:
        for disk in tmp_wmi.Win32_LogicalDisk():
            if disk.DeviceID == "C:":
                ret_VolumeSerialNumber = disk.VolumeSerialNumber
                break
            # End if
        # End for
    except Exception as e:
        print(e)
        ret_VolumeSerialNumber = "ERROR"
    finally:
        return ret_VolumeSerialNumber


def get_disk_info():
    """
    テスト関数
    """
    info_ = []
    myWmi = wmi.WMI()

    for disk in myWmi.Win32_LogicalDisk():
        info = {
            "diskName": disk.DeviceID,
            "freeSizes": int(int(disk.FreeSpace) / 1024 / 1024),
            "totalSizes": int(int(disk.Size) / 1024 / 1024),
        }
        info = disk.DeviceID
        info_.append(info)
        if disk.DeviceID == "C:":
            print(disk.VolumeSerialNumber)

    return info_


def get_disk_info2():
    """
    テスト関数
    """
    tmplist = []
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        tmpdict = {}
        tmpdict["capcity"] = int(physical_disk.Size) / 1024
        tmpdict["name"] = physical_disk.Caption
        tmplist.append(tmpdict)
    return {"result": tmplist}


class MyAESClass:
    def __init__(self):
        self.str_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # ランダムな文字列(32文字) : 暗号化キー
        self.str_iv = "XXXXXXXXXXXXXXXX"  # ランダムな文字列(16文字) : 初期化ベクトル
        self.key = self.str_key.encode()
        self.iv = self.str_iv.encode()

    # End def

    def encrypt_key(self, data: str):
        """
        文字列を暗号化し、暗号化された文字列を返す関数

        Parameters
        ----------
        data: str
            暗号化したい文字列

        Returns
        -------
        ct : str
            暗号化された文字列(cipher text)
        """
        data_byte = data.encode("utf-8")
        my_cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ct_bytes = my_cipher.encrypt(pad(data_byte, AES.block_size))
        ct = base64.b64encode(ct_bytes).decode("utf-8")
        return ct

    def decrypt_key(self, data):
        """
        暗号化された文字列を復号化し、文字列を返す。

        Parameters
        ----------
        data: str
            復号化したい、暗号化された文字列

        Returns
        -------
        pt : str
            復号化された文字列
        """
        try:
            ct = base64.b64decode(data.encode("utf-8"))
            my_cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            pt_byte = unpad(my_cipher.decrypt(ct), AES.block_size)
            pt = (pt_byte).decode("utf-8")
        except Exception as e:
            pt = "ERROR"
            print("ERROR")
            print(e)
        finally:
            return pt


def main():
    ret_VolumeSerialNumber = get_volume_serial_number()
    print(f"VolumeSerialNumber : {ret_VolumeSerialNumber}")
    my_aes = MyAESClass()
    ret_ct = my_aes.encrypt_key(ret_VolumeSerialNumber)
    print(f"暗号化キー : {ret_ct}")
    ret_pt = my_aes.decrypt_key(ret_ct)
    print(f"復号化された文字列 : {ret_pt}")


if __name__ == "__main__":
    main()
